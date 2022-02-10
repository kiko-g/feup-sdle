#import time

#from p2p.ntp import ntp_time
from zmq.sugar.constants import NULL


class Tweet:
    def __init__(self, author_id, author_username, text, post_time):
        self.author_id = author_id
        self.author_username = author_username
        self.text = text
        self.post_time = post_time
        self.rcv_time = NULL

    def __eq__(self, o: object) -> bool:
        return self.author_id == o.author_id and self.text == o.text and self.post_time == o.post_time \
               and self.author_username == o.author_username

    def to_dict(self):
        return {
            'author_id': self.author_id,
            'text': self.text,
            'author_username': self.author_username,
            'post_time': self.post_time,
            'rcv_time': self.rcv_time
        }
