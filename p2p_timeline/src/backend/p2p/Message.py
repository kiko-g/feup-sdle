from p2p.Timeline import Timeline
from p2p.Header import Header


class Message:
    def __init__(self, header: Header, body=None):
        self.header = header
        self.body = body

    @staticmethod
    def create_subscribe_msg(origin_ip_address, origin_port, origin_identifier, origin_username):
        return Message(
            Header('SUBSCRIBE'),
            {
                'origin_ip_address': origin_ip_address,
                'origin_port': origin_port,
                'origin_identifier': origin_identifier,
                'origin_username': origin_username
            }
        )

    @staticmethod
    def create_unsubscribe_msg(origin_ip_address, origin_username, origin_port, origin_identifier):
        return Message(
            Header('UNSUBSCRIBE'),
            {
                'origin_ip_address': origin_ip_address,
                'origin_port': origin_port,
                'origin_username': origin_username,
                'origin_identifier': origin_identifier
            }
        )

    @staticmethod
    def create_subscribe_indirect_msg(origin_ip_address, origin_port, origin_identifier, desired_identifier,
                                      desired_username,
                                      time_to_live: int = 4):
        return Message(
            Header('SUBSCRIBE_INDIRECT'),
            {'origin_ip_address': origin_ip_address, 'origin_port': origin_port, 'origin_identifier': origin_identifier,
             'desired_identifier': desired_identifier,
             'time_to_live': time_to_live,
             'desired_username': desired_username
             }
        )

    @staticmethod
    def create_subscribe_indirect_ack_msg(origin_ip_address, origin_port, origin_identifier, desired_ip_address,
                                          desired_port, desired_identifier, desired_username,
                                          timeline):
        return Message(
            Header('SUBSCRIBE_INDIRECT_ACK'),
            {'origin_ip_address': origin_ip_address, 'origin_port': origin_port, 'origin_identifier': origin_identifier,
             'desired_identifier': desired_identifier,
             'desired_ip_address': desired_ip_address,
             'desired_port': desired_port,
             'desired_username': desired_username,
             'timeline': timeline,
             }
        )

    @staticmethod
    def create_dummy_msg():
        return Message(
            Header('DUMMY'),
        )

    @staticmethod
    def create_ping_msg(origin_id, username, peer_id, origin_ip_address, origin_port):
        return Message(
            Header('PING', origin_id),
            {
                'peer_id': peer_id,
                'username': username,
                'origin_ip_address': origin_ip_address,
                'origin_port': origin_port
            }
        )

    @staticmethod
    def create_share_entity_msg(origin_id, peer_id, peer_username, peer_ip, peer_port):
        return Message(
            Header('SHARE_ENTITY', origin_id),
            {
                'peer_id': peer_id,
                'peer_ip': peer_ip,
                'peer_username': peer_username,
                'peer_port': peer_port
            }
        )

    @staticmethod
    def create_timeline_msg(origin_id, username, timeline: Timeline):
        return Message(
            Header('TIMELINE', origin_id),
            body={
                'username': username,
                'timeline': timeline,
            }
        )

    @staticmethod
    def create_users_msg(users: list):
        return Message(
            Header('USERS'),
            body={
                'users': users
            }
        )
