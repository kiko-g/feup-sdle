import asyncio
import pickle
import socket
import threading

import zmq
from kademlia.network import Server

from p2p.Logger import Logger
from p2p.ProcessMessage import process_message
from p2p.Protocol import *
from p2p.Subscriber import Subscriber
from p2p.TimeCounters import TimeCounters
from p2p.Timeline import Timeline
from p2p.Tweet import Tweet
from p2p.constants import DATA_PORT_OFFSET, FLASK_PORT_OFFSET

import time
from p2p.ntp import ntp_time


class Peer:
    def __init__(self, peer_id: int, remote_bootstrap_port: int, remote_bootstrap_ip='127.0.0.1',
                 host_ip='127.0.0.1'):
        self.identifier = peer_id
        self.username = ""
        self.kademlia_server = Server()
        self.logger = Logger(self.identifier)
        self.bootstrap_ip = remote_bootstrap_ip
        self.host_ip = host_ip
        self.data_port = DATA_PORT_OFFSET + self.identifier
        self.bootstrap_port = remote_bootstrap_port

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.zero_mq_context = zmq.Context()

        self.data_server_socket = self.zero_mq_context.socket(zmq.REP)

        self.followers = []

        self.neighbours = []

        self.followings = []

        self.zombies = []

        self.timelines = {self.identifier: Timeline(
            self.identifier, self.host_ip, self.data_port)}

        self.time_counter = TimeCounters()

        self.timestamp_ntp_request = 0

        self.time_delay = 0

        self.alive = True

    # TODO:Multiple bootstrap nodes
    async def init_kademlia_server(self):
        await self.kademlia_server.listen(self.data_port + 1000)
        await self.kademlia_server.bootstrap([(self.bootstrap_ip, self.bootstrap_port)])
        await self.kademlia_server.set(self.identifier,
                                       DHTEntry(self.identifier, self.host_ip, self.data_port).to_json())

    def bootstrap_users(self):

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.connect((self.host_ip, FLASK_PORT_OFFSET - 1))
        soc.sendall(pickle.dumps(Message.create_dummy_msg()))
        data = soc.recv(4096)

        if not data:
            print("Error Fetching users")
            exit(-1)

        message = pickle.loads(data)

        for user in message:
            sub = Subscriber(int(user['id']), user['username'], self.host_ip, int(user['id']) + DATA_PORT_OFFSET)

            if sub.identifier == self.identifier:
                self.username = sub.username
                continue

            if sub in self.neighbours:
                continue

            self.neighbours.append(sub)

        soc.close()

    async def run(self):
        self.bootstrap_users()

        await self.init_kademlia_server()

        t1 = threading.Thread(target=self.listen)
        t2 = threading.Thread(target=self.speak)

        t1.start()
        t2.start()

        while self.alive:
            await sleep(1)
            self.delete_tweet()

        t1.join()
        t2.join()

        self.kademlia_server.stop()

        print("Goodbye")

    def listen(self):
        asyncio.run(self.read_msgs_available())

    def speak(self):
        asyncio.run(gossiping(self))

    async def read_msgs_available(self):
        self.data_server_socket.bind(f"tcp://*:{self.data_port}")

        self.data_server_socket.setsockopt(zmq.SNDTIMEO, 30000)

        while self.alive:
            try:
                message = self.data_server_socket.recv_pyobj()

                self.data_server_socket.send_pyobj(Message.create_dummy_msg())

                if message is None:
                    continue

                threading.Thread(target=self.worker, args=(message,)).start()

            except Exception as e:
                print(e)
                print(f"{self.identifier}|Timeout SEND AFTER READ")

        self.data_server_socket.close()

    def worker(self, message):
        asyncio.run(process_message(self, message))

    async def subscribe(self, request):

        sub = Subscriber(request['identifier'], request['username'], request['host_ip'], request['data_port'])

        if sub in self.zombies:
            return await self.find_alternative_for_zombie(sub)

        dht_entry = DHTEntry.from_json(await self.kademlia_server.get(int(sub.identifier)))

        if not dht_entry:
            self.logger.print_error_subscriber()
            return
        try:
            self.send_subscribe_message(sub, dht_entry)
        except:
            pass

    def send_subscribe_message(self, sub: Subscriber, dht_entry: DHTEntry):

        self.send_message(dht_entry.ip_address, dht_entry.port,
                          Message.create_subscribe_msg(self.host_ip, self.data_port, self.identifier, self.username))

        if sub in self.neighbours:
            self.neighbours.remove(sub)

        if sub in self.followings:
            print(f"Already following")
            return

        self.followings.append(sub)

        self.timelines[sub.identifier] = Timeline(sub.identifier, sub.host_ip, sub.data_port)

        self.logger.print_new_following(sub)

    async def tweet(self, request):

        if self.time_counter.can_make_ntp_request(self.timestamp_ntp_request):
            self.timestamp_ntp_request = time.time()
            self.time_delay = ntp_time()

        post_time = time.time() + self.time_delay

        tweet = Tweet(self.identifier, self.username, request['text'], post_time)
        self.timelines[self.identifier].list_tweets.append(tweet)

    def send_message(self, ip_address: str, port: int, message: Message):
        self.logger.print_send_msg(ip_address, port, message)

        client_socket = self.zero_mq_context.socket(zmq.REQ)

        client_socket.connect(f"tcp://{ip_address}:{port}")

        client_socket.setsockopt(zmq.RCVTIMEO, 1000)
        client_socket.setsockopt(zmq.SNDTIMEO, 1000)

        client_socket.send_pyobj(message)
        client_socket.recv_pyobj()

        client_socket.close()

    async def find_alternative_for_zombie(self, zombie_sub: Subscriber):

        for neighbour in self.neighbours:

            if neighbour.identifier == zombie_sub.identifier:
                continue
            try:
                self.send_message(neighbour.host_ip, neighbour.data_port,
                                  Message.create_subscribe_indirect_msg(self.host_ip, self.data_port, self.identifier,
                                                                        zombie_sub.identifier, zombie_sub.username))
            except Exception as e:
                print(e)

    def logout(self):
        self.logger.print_logout()
        self.alive = False

    def delete_tweet(self):
        for author_id in self.timelines:
            if author_id != self.identifier:
                for tweet in self.timelines[author_id].list_tweets:
                    if self.time_counter.can_delete_tweet(tweet.rcv_time):
                        self.timelines[author_id].list_tweets.remove(tweet)

    async def unsubscribe(self, request):

        sub = Subscriber(request['identifier'], request['username'], request['host_ip'], request['data_port'])

        dht_entry = DHTEntry.from_json(await self.kademlia_server.get(int(sub.identifier)))

        if not dht_entry:
            self.logger.print_error_subscriber()
            return
        try:
            self.send_unsubscribe_message(sub, dht_entry)
            self.followings.remove(sub)
        except Exception as e:
            print(e)
            pass

    def send_unsubscribe_message(self, sub: Subscriber, dht_entry: DHTEntry):

        self.send_message(dht_entry.ip_address, dht_entry.port,
                          Message.create_unsubscribe_msg(self.host_ip, self.username, self.data_port, self.identifier))

        del self.timelines[sub.identifier]

        self.logger.print_new_unfollower(sub)
