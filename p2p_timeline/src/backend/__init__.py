import asyncio
import multiprocessing
import os
import sys
import threading
from time import sleep

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'p2p'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'server'))

from server.app import app
from server.app import set_peer

from p2p.BootstrapNode import BootstrapNode
from p2p.Peer import Peer
from p2p.constants import BOOTSTRAP_PORT_OFFSET, FLASK_PORT_OFFSET


def run_thread(peer):
    asyncio.run(peer.run())


def run_server_2(index, peer):
    set_peer(peer)

    app.run(host="127.0.0.1", port=FLASK_PORT_OFFSET + index, threaded=True)


def run_server(index):
    peer = Peer(index, BOOTSTRAP_PORT_OFFSET + 1)

    t1 = threading.Thread(target=run_thread, args=(peer,))
    t2 = threading.Thread(target=run_server_2, args=(index, peer,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    bootstrap_node_1 = BootstrapNode(1)

    threading.Thread(target=bootstrap_node_1.run).start()

    sleep(1)

    for index in range(1, 10):
        multiprocessing.Process(target=run_server, args=(index,)).start()
