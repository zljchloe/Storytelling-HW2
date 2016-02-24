#!/usr/bin/python

# redis package needs to be imported as we need to read data from redis database.
import redis
# json package needs to be imported as data needs to be loaded into json style.
import json
# time package needs to be imported as we need to use time.sleep.
import time
# sys package needs to be imported as data needs to be printed.
import sys

# Set a connection to redis database.
conn = redis.Redis()

# Continuously print out data.
while 1:
    # Enable pipeline to allow buffering multiple commands to the redis server to enhance the performance.
    pipe = conn.pipeline()
    # Set keys (time stamps) in redis database as keys.
    keys = conn.keys()
    # Set values (time differences) in redis database as values.
    values = conn.mget(keys)

    try:
        # Store values (time differences) in deltas as an array.
        deltas = [float(v) for v in values]
    except TypeError:
        # Handle TypeError condition
        print keys
        continue

    # if deltas contains any values (time differences), calculate rate, else rate is 0.
    if len(deltas):
        # calculate sum of values (time differences) divided by number of values,
        # which is the rate of data stream,
        # also considered as average time for generating new tweet.
        rate = sum(deltas)/float(len(deltas))
    else:
        rate = 0

    # if rate>10, means the keyword has been showing up frequently, print out the alert message. 
    if rate>10:
        print (json.dumps({"rate":rate}), "there might be an earthquake happening somewhere!")
        sys.stdout.flush()
    # else show no alert message.
    else:
        print json.dumps({"rate":rate})
        sys.stdout.flush()

    # set 1 sec sleep time between each iteration.
    time.sleep(1)