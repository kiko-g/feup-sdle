import asyncio
import logging

from kademlia.network import Server

from p2p.constants import BOOTSTRAP_PORT_OFFSET


class BootstrapNode:
    def __init__(self, peer_id: int, port=None):
        self.peer_id = peer_id
        self.debug = False
        if port:
            self.port = port
        else:
            self.port = BOOTSTRAP_PORT_OFFSET + self.peer_id

    def run(self):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if self.debug:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            log = logging.getLogger('kademlia')
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)
            loop.set_debug(True)

        server = Server()
        loop.run_until_complete(server.listen(self.port))

        try:
            loop.run_forever()
        finally:
            server.stop()
            loop.close()
