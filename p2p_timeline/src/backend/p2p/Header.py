class Header:
    def __init__(self, msg_type: str, origin_id: int = None):
        self.type = msg_type
        self.origin_id = origin_id
