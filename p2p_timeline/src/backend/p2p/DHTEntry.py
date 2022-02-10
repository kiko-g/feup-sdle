import json


class DHTEntry:

    def __init__(self, identifier: int, ip_address: str, port: int):
        self.identifier = identifier
        self.ip_address = ip_address
        self.port = port

    def to_json(self):
        return json.dumps({
            'identifier': self.identifier,
            'ip_address': self.ip_address,
            'port': self.port,
        })

    @staticmethod
    def from_json(json_str):
        if not json_str:
            return None

        json_obj = json.loads(json_str)

        return DHTEntry(json_obj['identifier'], json_obj['ip_address'], json_obj['port'])
