from p2p.Subscriber import Subscriber
from p2p.Message import Message


class Logger:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.logs_disabled = False

    def prefix(self):
        return f"[ID:{self.peer_id}]|"

    def print_heartbeat(self):
        if self.logs_disabled:
            return
        print(f"{self.prefix()}ALIVE")

    def print_send_msg(self, ip_address, port, message: Message):
        if self.logs_disabled:
            return

        if message.header.type == 'PING' or message.header.type == 'SHARE_ENTITY':
            pass
            # print(f"{self.prefix()}Send PING:ID{message.body['peer_id']} To {ip_address}:{port}")
        else:
            print(f"{self.prefix()}Send MSG:{message.header.type} To {ip_address}:{port}")

    def print_msg_received(self, message: Message):
        if self.logs_disabled:
            return

        if message.header.type == 'PING' or message.header.type == 'SHARE_ENTITY':
            pass
            # print(
            #   f"{self.prefix()}Received {message.header.type} MSG: PEER_ID {message.body['peer_id']} FROM:{message.header.origin_id}")
        else:
            print(f"{self.prefix()}Received MSG:{message.header.type}")

    def print_error_subscriber(self):

        if self.logs_disabled:
            return

        print(f"{self.prefix()}ERROR")

    def print_new_follower(self, follower: Subscriber):
        if self.logs_disabled:
            return

        print(f"{self.prefix()} FOLLOWED BY:{follower.identifier}")

    def print_new_unfollower(self, following: Subscriber):
        if self.logs_disabled:
            return

        print(f"{self.prefix()} UNFOLLOWED BY:{following.identifier}")

    def print_new_following(self, following: Subscriber):
        if self.logs_disabled:
            return

        print(f"{self.prefix()} FOLLOWING:{following.identifier}")

    def print_timeline_non_following(self, message: Message):
        if self.logs_disabled:
            return
        print(f"{self.prefix()}RECEIVED TIMELINE I DONT FOLLOW.TODO PROTOCOL")

    def print_neighbour_died(self, dead_peer: Subscriber):
        if self.logs_disabled:
            return
        print(f"{self.prefix()}DIED {dead_peer.identifier}")

    def print_found_alternative_for_zombie(self, remote_following, zombie_sub):
        if self.logs_disabled:
            return
        print(f"{self.prefix()}FOUND ALTERNATIVE IN {remote_following.identifier} FOR ZOMBIE {zombie_sub.identifier}")

    def print_address_not_open(self, ip_address, port):
        if self.logs_disabled:
            return
        print(f"{self.prefix()} DIDN'T SEND TO {ip_address}:{port} PORT CLOSED")

    def print_logout(self):
        if self.logs_disabled:
            return
        print(f"{self.prefix()}LOGOUT")

    def print_peer_back_online(self, neighbour):
        # if self.logs_disabled:
        #   return

        print(f"{self.prefix()}|{neighbour.identifier} BACK ONLINE")
