import random
import time

from asyncio import sleep

from p2p.DHTEntry import DHTEntry
from p2p.Message import Message
from p2p.Subscriber import Subscriber
from p2p.Timeline import Timeline
from p2p.constants import BOOTSTRAP_PORT_OFFSET


async def process_message(peer, message: Message):
    peer.logger.print_msg_received(message)
    # TODO:REMOVE FROM ZOMBIE
    if message.header.type == 'PING':
        return await process_ping_message(peer, message)

    if message.header.type == 'SHARE_ENTITY':
        return await process_share_entity_message(peer, message)

    if message.header.type == 'SUBSCRIBE':
        return process_subscribe_message(peer, message)

    if message.header.type == 'UNSUBSCRIBE':
        return process_unsubscribe_message(peer, message)

    if message.header.type == 'SUBSCRIBE_INDIRECT':
        return await process_subscribe_indirect_message(peer, message)

    if message.header.type == 'SUBSCRIBE_INDIRECT_ACK':
        return process_subscribe_indirect_ack_message(peer, message)

    if message.header.type == 'TIMELINE':
        return process_timeline_message(peer, message)


async def process_ping_message(peer, message: Message):
    neighbour = Subscriber(message.body['peer_id'], message.body['username'], message.body['origin_ip_address'],
                           message.body['origin_port'])

    if peer.identifier == neighbour.identifier:
        return

    if neighbour in peer.zombies:
        peer.logger.print_peer_back_online(neighbour)

        if neighbour in peer.followings:
            dht_entry = DHTEntry.from_json(await peer.kademlia_server.get(neighbour.identifier))

            if not dht_entry:
                return

            peer.send_subscribe_message(neighbour, dht_entry)

        peer.zombies.remove(neighbour)

    if neighbour in peer.neighbours:
        return

    if neighbour in peer.followings:
        return

    if neighbour.data_port >= BOOTSTRAP_PORT_OFFSET:
        return

    peer.neighbours.append(neighbour)


async def process_share_entity_message(peer, message):
    neighbour = Subscriber(message.body['peer_id'], message.body['peer_username'], message.body['peer_ip'],
                           message.body['peer_port'])

    if peer.identifier == neighbour.identifier:
        return

    if neighbour in peer.neighbours:
        return

    if neighbour in peer.followings:
        return

    if neighbour.data_port >= BOOTSTRAP_PORT_OFFSET:
        return

    peer.neighbours.append(neighbour)


def process_subscribe_message(peer, message: Message):
    sub = Subscriber(message.body['origin_identifier'], message.body['origin_username'],
                     message.body['origin_ip_address'],
                     message.body['origin_port'])

    if sub in peer.neighbours:
        peer.neighbours.remove(sub)

    if sub not in peer.followers:
        peer.followers.append(sub)
        peer.logger.print_new_follower(sub)
    else:
        print(f"Already Following")


def process_unsubscribe_message(peer, message: Message):
    sub = Subscriber(message.body['origin_identifier'], message.body['origin_username'],
                     message.body['origin_ip_address'],
                     message.body['origin_port'])

    if sub not in peer.neighbours:
        peer.neighbours.append(sub)
    else:
        print(f"Already in Neighbours")
    if sub in peer.followers:
        peer.followers.remove(sub)
        peer.logger.print_new_unfollower(sub)
    else:
        print(f"Already NOT following")


async def process_subscribe_indirect_message(peer, message):
    desired_sub = message.body['desired_identifier']
    desired_username = message.body['desired_username']

    if desired_sub in peer.timelines.keys():
        reply = Message.create_subscribe_indirect_ack_msg(peer.host_ip, peer.data_port,
                                                          peer.identifier, peer.timelines[desired_sub].host_ip,
                                                          peer.timelines[desired_sub].port,
                                                          desired_sub, desired_username,
                                                          peer.timelines[desired_sub].list_tweets)

        return peer.send_message(message.body['origin_ip_address'], message.body['origin_port'], reply)
    else:
        if int(message.body['time_to_live'] == 0):
            print("MSG Expired")
            return

        if len(peer.neighbours) == 0:
            return

        for i in range(3):
            neighbour = random.choice(peer.neighbours)

            if neighbour.identifier == int(message.body['origin_identifier']):
                continue
            if neighbour.identifier == int(message.body['desired_identifier']):
                continue
            try:
                peer.send_message(neighbour.host_ip, neighbour.data_port,
                                  Message.create_subscribe_indirect_msg(message.body['origin_ip_address'],
                                                                        message.body['origin_port'],
                                                                        message.body['origin_identifier'],
                                                                        message.body['desired_identifier'],
                                                                        message.body['desired_username'],
                                                                        int(message.body['time_to_live']) - 1))
            except:
                pass

            await sleep(0.1)


def process_subscribe_indirect_ack_message(peer, message):
    sub = Subscriber(message.body['desired_identifier'],
                     message.body['desired_username'],
                     message.body['desired_ip_address'],
                     message.body['desired_port'],
                     int(message.body['origin_identifier']),
                     message.body['origin_ip_address'],
                     message.body['origin_port'])

    if sub in peer.followings:
        return

    peer.followings.append(sub)

    if sub in peer.neighbours:
        peer.neighbours.remove(sub)

    print("Received Timeline from third party")

    peer.timelines[sub.identifier] = Timeline(
        sub.identifier, sub.host_ip, sub.data_port, message.body['timeline'])


def process_timeline_message(peer, message: Message):
    timeline = message.body['timeline']

    for following in peer.followings:
        if following.identifier == timeline.author_id:
            return process_timeline_from_following(peer, message)


def process_timeline_from_following(peer, message: Message):
    timeline = message.body['timeline']

    # Don't update my timeline with others
    if timeline.author_id != peer.identifier:
        return process_timeline_new_tweets(peer, message)


def process_timeline_new_tweets(peer, message: Message):
    timeline = message.body['timeline']
    rcv_time = time.time()
    for tweet in timeline.list_tweets:

        if tweet not in peer.timelines[timeline.author_id].list_tweets:
            tweet.rcv_time = rcv_time
            peer.timelines[timeline.author_id].list_tweets.append(tweet)
