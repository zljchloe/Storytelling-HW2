# Storytelling-HW2
HW2 aims to calculate rate of a stream of data, in this case we are calculating rate of the twitter stream.

## Installation
1. Install `python 2.7`
2. Install `tweepy` package from source, you can use command as following:
<pre><code>git clone git://github.com/tweepy/tweepy.git
cd tweepy
python setup.py install</prev></code>
3. Install `numpy` package, you can use command as following: `sudo pip install numpy`
4. Install `redis` package, you can use command as following: `sudo pip install redis`
5. Install `websocketd`

## Usage

### poll-twitter.py
- Simply run <pre><code>python poll-twitter.py</pre></code>
- The output of this file is the time stamp of each generated tweet. 
- We used `numpy` package to generate random time of sleep according to exponential function, to stimulate a poisson process. 
- `tweepy` package is also used in this file, because we are polling twitter streaming API here to get the streamed tweet. 
- The keyword in this file is set to be `earthquake`, so we are getting the time stamp of streamed tweet which has mentioned `earthquake`.  

### diff.py
- Run `diff.py` with the output of `poll-twitter.py` piped to it. More explicitly, run <pre><code>poll-twitter.py | diff.py</pre></code>
- We took the output of `poll-tweepy.py` and calculate the time difference of each streamed data.
- The output of this file is the time difference of each streamed tweet, together with its own time stamp.  

### insert.py
- Run `insert.py` with the output of `diff.py` piped to it. More explicitly, run <pre><code>poll-twitter.py | diff.py | insert.py</pre></code>
- The purpose of this file is to insert the result of `diff.py` to redis database. We set the time stamp as the key, and the time difference as the value associated with the key, and then store them in the redis database.  

### avg.py
- Run `avg.py` together with running `insert.py`. More explicitly, run 
<pre><code>poll-twitter.py | diff.py | insert.py
python avg.py</pre></code>
- We are calculating rate of twitter stream in this file, by reading from redis database. The rate can be calculated in this way:
<pre><code>rate = sum(time difference) / number of records</pre></code>
Where time difference is the value stored in the redis database. `number of records` would go up by time, and drop down when it reaches expiration time we set in `insert.py` file.
- An alert has been set up, which is when keyword `earthquake` is being mentioned in a relativly high rate, an alert message would be generated, telling people there might be an actual earthquake happening somewhere.  

### index.html
- To connect the alert system into a human-readable system, we need to use `websocketd` to transfer the messages into a web page.
- Run <pre><code>poll-twitter.py | diff.py | insert.py
websocketd --port=8080 ./avg.py</pre></code> And open `index.html`, we will see the message is now being printed to a web page.
- When alert is off, the webpage simply prints out each time stamp of generated tweet. And when the rate of streaming exceeds a certain threshold (in this case we set `rate>10`), an alert message would pop up saying "there might be an earthquake happening somewhere!"  