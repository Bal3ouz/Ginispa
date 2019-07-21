#principal


from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
import csv
import json



# # # # TWITTER authenticator  # # # #
class TwitterAuthenticator():

    def authenticate(self):

        consumer_key = 'MmKd7ilt9lrCZu6HfQcZI6Woq'
        consumer_secret = '88Iemv96p77WqOaf4OHPUrv3DmZqYpiWsOFJisN492X133nW6k'
        access_token = '1147519079764451334-BqavD1cJuyZavcNgcqOhYo2jbB9W19'
        access_token_secret = '4dLqGH8AwUt01BB6DS46c5d3lKXG1Yd8PRQX7Vb706Iu2'
        # create authentication for accessing Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth


# # # # TWITTER Client ( tweets of specific person)  # # # #

class TwitterClient():

    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_client = tweepy.API(self.auth)


    def get_user_tweets(self, twitter_user, num_tweets):
        tweets=[]
        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, id=twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_hashtag_tweets(self, hashtag):
        tweets=[]
        #get api
        api = tweepy.API(TwitterAuthenticator().authenticate())
         #constructing list of tweets matching hashtag

        for tweet in tweepy.Cursor(api.search, q=hashtag, lang="en", tweet_mode="extended").items(100):
            tweets.append(tweet)
        return tweets



# # # # TWITTER Analyzer # # # #

class TweetAnalyzer():

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])


        return df

    def clean_tweet(self, tweet_text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet_text).split())

    def analyze_sentiment(self,tweet_text):
        analysis = TextBlob(self.clean_tweet(tweet_text))
        return analysis.sentiment.polarity

    def tweets_to_csv_file(self,tweets):

        with open('result.csv', 'w') as file:
            w = csv.writer(file)
            # write header row to spreadsheet
            w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'likes','location'])
            for tweet in tweets:
                w.writerow([tweet.created_at, tweet.full_text.encode('utf-8'), tweet.user.screen_name,[e['text'] for e in tweet._json['entities']['hashtags']], tweet.favorite_count,tweet.user.location])

        # # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, hash_tag_list):

        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener()
        auth = TwitterAuthenticator().authenticate()
        stream = Stream(auth=auth, listener=listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """


    def __init__(self):
        pass

    def on_data(self, data):
        try:
            print(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == '__main__':
    #streaming tweets with hashtag list :

    #streamer = TwitterStreamer()
    #hash_tag_list = ["tunisie"]
    #tweets = streamer.stream_tweets(hash_tag_list)



    #getting data frame of tweets :

    t=TweetAnalyzer()
    tweets = TwitterClient().get_hashtag_tweets('#ennahdha')
    #example of getting user tweets :
    #tweets_user = TwitterClient().get_user_tweets('id of user ', 'number of tweets ')
    df = t.tweets_to_data_frame(tweets)
    print(df )



