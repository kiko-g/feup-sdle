import path
import sys
directory = path.path(__file__).abspath()
sys.path.append(directory.parent)
from messages.message import Message


import zmq

from messages.message import Message
from messages.message_factory import MessageFactory
from proxy.clients_list_record import ClientListRecord
from proxy.message_list_record import MessageListRecord
from proxy.utils import *

context = zmq.Context()


class Proxy:
    def __init__(self, xpub_port: int = 5555, xsub_port: int = 5556, rep_port: int = 6789) -> None:

        self.xpub_address = f'tcp://127.0.0.1:{xpub_port}'
        self.xsub_address = f'tcp://127.0.0.1:{xsub_port}'
        self.rep_address = f'tcp://127.0.0.1:{rep_port}'

        self.clients = {}
        self.messages = {}

        # create XPUB
        self.xpub_socket = context.socket(zmq.XPUB)
        self.xpub_socket.bind(self.xpub_address)

        # create XSUB
        self.xsub_socket = context.socket(zmq.XSUB)
        self.xsub_socket.bind(self.xsub_address)

        # create REP
        self.rep_socket = context.socket(zmq.REP)
        self.rep_socket.bind(self.rep_address)

        # create poller
        self.poller = zmq.Poller()
        self.poller.register(self.xpub_socket, zmq.POLLIN)
        self.poller.register(self.xsub_socket, zmq.POLLIN)
        self.poller.register(self.rep_socket, zmq.POLLIN)


if __name__ == "__main__":
    proxy = Proxy(sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else Proxy()
    proxy.run()
