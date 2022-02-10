import time


class TimeCounters:
    def __init__(self):
        self.timestamp_last_entity_exchange = 0.0
        self.seconds_between_entity_exchange = 10.0
        self.seconds_for_msg_receiving = 0.5
        self.sleep_between_iterations = 0.5
        self.timestamp_last_gossip_test = 0.0
        self.seconds_between_test_exchange = 15.0
        self.timestamp_last_timelines = 0.0
        self.seconds_between_timelines_exchange = 10.0
        self.seconds_to_delete_tweet = 5000000.0
        self.seconds_between_ntp_requests = 300.0

    def can_gossip_entity(self) -> bool:
        current_timestamp = time.time()

        if current_timestamp >= self.timestamp_last_entity_exchange + self.seconds_between_entity_exchange:
            self.timestamp_last_entity_exchange = current_timestamp
            return True

        return False

    def can_gossip_test(self):
        current_timestamp = time.time()

        if current_timestamp >= self.timestamp_last_gossip_test + self.seconds_between_test_exchange:
            self.timestamp_last_gossip_test = current_timestamp
            return True

        return False

    def can_gossip_timelines(self):
        current_timestamp = time.time()

        if current_timestamp >= self.timestamp_last_timelines + self.seconds_between_timelines_exchange:
            self.timestamp_last_timelines = current_timestamp
            return True

        return False

    def reduce_interval_entity_exchange(self):

        if self.seconds_between_entity_exchange <= 1:
            self.seconds_between_entity_exchange = 1
        else:
            self.seconds_between_entity_exchange -= 0.5

    def increase_interval_entity_exchange(self):
        if self.seconds_between_entity_exchange >= 20:
            self.seconds_between_entity_exchange = 20
        else:
            self.seconds_between_entity_exchange += 2

    def can_receive_msgs(self, first_timestamp) -> bool:

        if time.time() >= first_timestamp + self.seconds_for_msg_receiving:
            return False

        return True

    def can_delete_tweet(self, rcv_time):
        current_time = time.time()

        if current_time >= (rcv_time + self.seconds_to_delete_tweet):
            return True

        return False

    def can_make_ntp_request(self, timestamp_ntp_request):
        current_time = time.time()

        if current_time >= (timestamp_ntp_request + self.seconds_between_ntp_requests):
            return True

        return False
