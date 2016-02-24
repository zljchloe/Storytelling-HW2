#!/usr/bin/python

# json package needs to be imported as the data to be printed is in json format.
import json
# sys package needs to be imported as data needs to be printed.
import sys

# Set initial time as 0.
last = 0

# Continuously print out data.
while 1:
	# Read the time generated from poll-twitter.py file.
    line = sys.stdin.readline()
    # Reformat the data to json style.
    d = json.loads(line)
    # if the data is the first one that's passed in,
    # set the first data's time as last.
    if last == 0 :
        last = d["t"]
        continue
    # if the data is not the first one that's passed in,
    # calculate the difference of the current time value and the previous time value (stored in last).
    delta = d["t"] - last
    # Print out the time differenc and current time stamp.
    print json.dumps({"delta":delta, "t":d["t"]})
    sys.stdout.flush()
    # Set current time stamp to last for the next iteration.
    last = d["t"]