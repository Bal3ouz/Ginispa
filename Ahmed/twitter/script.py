#getting a csv file containig tweets with hashtag :


import tweepy
import csv
import sys
import re

consumer_key = 'MmKd7ilt9lrCZu6HfQcZI6Woq'
consumer_secret = '88Iemv96p77WqOaf4OHPUrv3DmZqYpiWsOFJisN492X133nW6k'
access_token = '1147519079764451334-BqavD1cJuyZavcNgcqOhYo2jbB9W19'
access_token_secret = '4dLqGH8AwUt01BB6DS46c5d3lKXG1Yd8PRQX7Vb706Iu2'

# create authentication for accessing Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#get the name of the spreadsheet we will write to
hashtag_phrase=sys.argv[1]
fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    #open the spreadsheet we will write to
with open('%s.csv' % (fname), 'w') as file:

    w = csv.writer(file)

    #write header row to spreadsheet
    w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

# initialize Tweepy APi
    tweets = tweepy.Cursor(api.search, q=hashtag_phrase, lang="en", tweet_mode="extended").items(100)
    for tweet in tweets:
        w.writerow([tweet.created_at, tweet.full_text.encode('utf-8'), tweet.user.screen_name, [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])

file.close()