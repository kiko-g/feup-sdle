from threading import Timer
from copy import copy


def list_clients_existent_at_give_time_for_give_topic(topic: str, clients: dict) -> list:
    list_to_return = []
    topic = topic

    if topic not in clients:
        return []

    for key in clients[topic]:
        list_to_return.append(copy(clients[topic][key].client_id))

    return list_to_return


def set_interval(action, interval=3, active=True):
    action()
    if active:
        Timer(
            interval,
            set_interval,
            kwargs={'action': action, 'interval': interval, 'active': active}
        ).start()
