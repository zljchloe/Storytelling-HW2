#!/usr/bin/python

# json package needs to be imported as the data needs to be loaded into json format.
import json
# sys package needs to be imported as the data needs to be printed out.
import sys
# redis package needs to be imported as data needs to be stored with redis.
import redis

# Initiate a database to store the previous information generated from diff.py.
conn = redis.Redis()

# Continuously print out the data.
while 1:
	# Read output value from diff.py,
	# which is each tweet's time difference and its own time stamp.
    line = sys.stdin.readline()
    # Reload the data in json style.
    d = json.loads(line)
    # Read the line and set time difference as delta.
    delta = d["delta"]
    # Read the line and set time stamp as time.
    time = d["t"]
    # Set time as key, delta as value, 120 as the expiration time in the redis database.
    conn.setex(time, delta, 120)
    # Print out time difference and time stam,
    # which as been stored in the database.
    print json.dumps({"time":time, "delta":delta})