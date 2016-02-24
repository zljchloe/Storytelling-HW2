#!/usr/bin/python

# poll-twitter.py polls twitter data from twitter streaming API.
# It shows real time twitter stream with keyword set inside the file, which is "earthquake" in this case.
# To stimulate a poisson process, we take exponential random generator into processing the stream.

# tweepy package needs to be imported with python as one of the library.
# tokens need to be verified upon calling the twitter API.
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
# sys package needs to be imported as data needs to be printed.
from sys import stdout
# json package needs to be imported as data needs to be presented in json format.
import json
# unicodedata package needs to be imported as UnicodeDataError needs to be handled.
import time
# numpy package needs to be imported as we need to distribute an exponential sleep time.
import numpy as np

# Please enter consumer key, consumer secret, access token, access secret.
ckey="Enter ckey"
csecret="Enter csecret"
atoken="Enter atoken"
asecret="Enter asecret"

# Set exponential function's parameter as rate, to pass into the np.random.exponential() function.
rate = 2

# Define listener class to process streaming data
class listener(StreamListener):

    # Define on_data function to print out the time stamp of each streamed tweet.
    # Set time.sleep to random number generated by exponential function to stimulate poisson process.
    def on_data(self, data):
        print json.dumps({"t": time.time()})
        stdout.flush()
        time.sleep(np.random.exponential(rate))
        return True

    # Define on_error function to handle disconnection error condition.
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print(status_code)
            return False

# Infinite loop to continuously print out streaming data.
while True:
    # Pass user entered ckey, csecret, atoken and asecret to verify authentication.
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

    # Create a stream with above verification information and listener class defined above.
	twitterStream = Stream(auth, listener())
    # Filter the stream's data with keyword set as "earthquake", so it shows tweet which mentions "earthquake".
	twitterStream.filter(track=["earthquake"])