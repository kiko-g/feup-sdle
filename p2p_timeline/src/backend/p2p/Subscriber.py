class Subscriber:
    def __init__(self, identifier: int, username: str, host_ip: str, data_port: str, indirection: int = None,
                 indirection_ip=None,
                 indirection_port=None):
        self.identifier = identifier
        self.username = username
        self.host_ip = host_ip
        self.data_port = data_port
        self.indirection = indirection
        self.indirection_ip = indirection_ip
        self.indirection_port = indirection_port

    def to_dict(self):
        return {
            'username': self.username,
            'identifier': self.identifier,
            'username': self.username,
            'host_ip': self.host_ip,
            'data_port': self.data_port,
            'indirection': self.indirection
        }

    def __eq__(self, o: object) -> bool:
        return self.identifier == o
