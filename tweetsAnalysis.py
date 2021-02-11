#!/usr/bin/env python
# coding: utf-8

# ### library imports

# In[7]:


import tweepy
# !pip install textblob
from textblob import TextBlob
# !pip install git+https://github.com/JustAnotherArchivist/snscrape.git
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import numpy as np


# ###### tweeter app api key & access token for tweepy

# In[3]:


consumer_key = "1TqW5hse6LaAxCCvzZgORWfhx"
consumer_secret = "lfE5MXH9C8GuhB9J8jeNlQSW9zSQ8zwbQAaZDWqwvz1CWSiEm0"
access_token = "435849217-BZdlW1rVPClgt8m1cXXJdqG6xmCnuJAy6ie5f1MR"
access_token_secret = "ojf8Ak3uvLpOcm6yykfAf11UYpjtood9PXGlDc8DJlqiU"


# In[4]:


# OAuthHandler object for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Sets access token and token secret
auth.set_access_token(access_token, access_token_secret)

# Creates API object by passing auth information
api = tweepy.API(auth)


# #### Task a: latest trending topic for India. (#tag and no of tweets for the particular #tag)

# In[92]:


# twitter india trends by woeid
india_woeid = 2282863
twitter_trends = api.trends_place(id=india_woeid)

trends_list = []

for trend in twitter_trends[0]['trends']:
    trends_list.append([trend['name'], trend['tweet_volume']])


# In[102]:


trends_df = pd.DataFrame(trends_list, columns=['#tags', 'Tweets Count'])
trends_df.to_csv('indian_trends.csv', encoding='utf-8', index=True)
trends_df.head(10)


# #### Task b:  Extract first 100 tweets for #JoeBiden

# In[91]:


query = '#JoeBiden'
count = 100

tweets_list = []

# querry twitter through sntwitter.TwitterSearchScraper and append each tweet to tweets_list array
for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > count:
        break
    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])


# In[103]:


# adds tweets_list to data frame
tweets_df = pd.DataFrame(tweets_list, columns=['Date', 'Tweet Id', 'Text', 'Username'])

# saves tweets in csv file
tweets_df.to_csv('100_biden_tweets.csv', encoding='utf-8', index=True)
tweets_df.head(9)


# #### Task c: Sentiment Analysis for #JoeBiden (Is it positive/negative, what is the perception)

# In[107]:


# Cleans tweet text by removing links, emails, etc
def clean_tweet_text(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())

tweets_df['Text'] = np.array([clean_tweet_text(tweet) for tweet in tweets_df['Text']])

# Analyse tweet & score 1 for positive, 0 for neutral & -1 for negative sentiment
def sentiment_analyzer(tweet):
    analysis = TextBlob(tweet)
    
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else: 
        return -1
    
tweets_df['sentiment'] = np.array([sentiment_analyzer(tweet) for tweet in tweets_df['Text']])

# saves tweets df with sentiment column to csv file
tweets_df.to_csv('biden_tweets_sentiments.csv', encoding='utf-8', index=True)

tweets_df.head(10)


# In[108]:


tweets_df['sentiment'].mean()


# ###### mean is < 1 & > 0 so sentiment is between neutral to positive
