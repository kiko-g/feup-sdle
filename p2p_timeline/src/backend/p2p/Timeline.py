class Timeline:
    def __init__(self, author_id, host_ip, port, list_tweets=None):
        if list_tweets is None:
            list_tweets = []

        self.author_id = author_id
        self.list_tweets = list_tweets
        self.host_ip = host_ip
        self.port = port
        

    def __eq__(self, o: object) -> bool:
        if self.author_id != o.author_id:
            return False

        if len(self.list_tweets) != o.list_tweets:
            return False

        # TODO:IMPROVE
        return True

    def to_dict(self):

        dict_list_tweets = []

        for tweet in self.list_tweets:
            dict_list_tweets.append(tweet.to_dict())

        return {
            'author_id': self.author_id,
            'list_tweets': dict_list_tweets
        }
