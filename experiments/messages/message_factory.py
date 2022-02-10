from messages.header import Header
from messages.message import Message


class MessageFactory:
    ####Messages

    @staticmethod
    def create_hello_message(id_origin: str, address_origin: str, topic: str):
        header = Header("hello")
        header.id_origin = id_origin
        header.address_origin = address_origin
        header.topic = topic

        return Message(header)

    @staticmethod
    def create_topic_message(topic: bytes, message_id: bytes, body: bytes):
        header = Header("data")
        header.topic = topic.decode()
        header.message_id = message_id.decode()

        return Message(header, body.decode())

    ####Replies

    @staticmethod
    def create_ack_welcome_reply():
        return Message(Header("ack_welcome"))

    @staticmethod
    def create_ack_received_reply(id_origin: str, message_id: bytes, topic: bytes):
        header = Header("ack_received")
        header.id_origin = id_origin
        header.message_id = message_id.decode()
        header.topic = topic.decode()
        return Message(header)
