#aanother code for streaming tweets :

import tweepy
class MyStreamListener(tweepy.StreamListener):

    def on_data(self, status):
        self.process_data(status)
        return True

    def process_data(self,status):
        print(status)

    def on_error(self, status_code):
        if status_code==420:
            return False

class MyStream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self, keyword_list):
        self.stream.filter(track=keyword_list)




if __name__ == '__main__':

    consumer_key = 'MmKd7ilt9lrCZu6HfQcZI6Woq'
    consumer_secret = '88Iemv96p77WqOaf4OHPUrv3DmZqYpiWsOFJisN492X133nW6k'
    access_token = '1147519079764451334-BqavD1cJuyZavcNgcqOhYo2jbB9W19'
    access_token_secret = '4dLqGH8AwUt01BB6DS46c5d3lKXG1Yd8PRQX7Vb706Iu2'

    # create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    listener = MyStreamListener()
    stream = MyStream(auth, listener)
    stream.start(['Beji caid Essebsi',''])