import sys

import asyncio
import threading
from time import sleep

from server.app import app
from server.app import set_peer

from p2p.BootstrapNode import BootstrapNode
from p2p.Peer import Peer
from p2p.constants import BOOTSTRAP_PORT_OFFSET, FLASK_PORT_OFFSET


def run_thread(peer):
    asyncio.run(peer.run())


def run_server_2(index, peer):
    set_peer(peer)

    app.run(host="127.0.0.1", port=FLASK_PORT_OFFSET + index)


def run_server(index):
    peer = Peer(index, BOOTSTRAP_PORT_OFFSET + 1)

    t1 = threading.Thread(target=run_thread, args=(peer,))
    t2 = threading.Thread(target=run_server_2, args=(index, peer,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':

    try:
        index = int(sys.argv[1])
    except:
        print('\n \n init_peer.py <peer_id>')
        sys.exit(2)

    t2 = threading.Thread(target=run_server, args=(index,))
    t2.start()

    t2.join()
