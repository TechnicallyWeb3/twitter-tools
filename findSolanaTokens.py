import re
import time
import winsound
import user

FOLLOW_USERS = ['TechnicallyWeb3']

solana_address_pattern = re.compile(r'[A-HJ-NP-Za-km-z1-9]{32,44}')

def makeNoise(bottom=200, beeps = 5):
    # make noise!
    for i in range(bottom, bottom+beeps):
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = i  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        time.sleep(0.1)

class User:
    def __init__(self, name):
        self.name = name
        self.id = self.get_id()
        self.tweet_count = 0
        self.tweets = []
        self.last_tweet = None

    def get_id(self):
        return user.get_user_ids(self.name)

    def get_tweet_count(self):
        tweet_count = user.get_tweet_count(self.name)
        if tweet_count is not None:
            self.tweet_count = tweet_count
        # print(self.tweet_count)
        return self.tweet_count

    def get_tweets(self):
        self.tweets = user.get_user_tweets(self.id)
        return self.tweets

    def __str__(self):
        return f"User(name={self.name}, id={self.id}, tweet_count={self.tweet_count}, tweets={self.tweets})"
    
class TwitterFeed:
    def __init__(self):
        self.follow_list = []

    def add_users_by_name(self, new_users):
        for name in new_users:
            self.add_user(User(name))
        return self
    
    def add_user(self, new_user):
        self.follow_list.append(new_user)
    
    def watch(self):
        users = self.follow_list

        while True:
            for u in users:
                last_count = u.tweet_count
                tweet_count = u.get_tweet_count()
                print(f"{u.name} tweet count = {tweet_count}")

                if last_count != tweet_count:
                    tweets = u.get_tweets()
                    for t in tweets:
                        if (solana_address_pattern.search(t['text'])):
                            print(f"Possible Match {t['text']}")
                            for address in solana_address_pattern.findall(t['text']):
                                print(f"Address found: {address}")
                            makeNoise(bottom=1000, beeps=60)
                    
                    print (f"Last Tweet {tweets[0]['created_at']}: {tweets[0]['text']}")


                    makeNoise()

feed = TwitterFeed().add_users_by_name(FOLLOW_USERS)
feed.watch()
