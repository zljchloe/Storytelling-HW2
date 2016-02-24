# Storytelling-HW2
HW2 aims for calculating rate of a stream of data, in this case we are calculating rate of the twitter stream.

## Installation
1. Install `python 2.7`
2. Install `tweepy` package from source, you can use command as following:
<pre><code>`git clone git://github.com/tweepy/tweepy.git`
`cd tweepy`
`python setup.py install`</prev></code>
3. Install `numpy` package, you can use command as following: `sudo pip install numpy`
4. Install `redis` package, you can use command as following: `sudo pip install redis`

## Usage
### poll-twitter.py
- Simply run `python poll-twitter.py`. 
- The output of this file is the time stamp of each generated tweet. We used `numpy` package to generate random time of sleep according to exponential function, to stimulate a poisson process. `tweepy` package is also used in this file, because we are polling twitter stream API here to get the streaming tweet. The keyword in this file is set to be "earthquake", so we are getting the time stamp of streamed tweet which has mentioned "earthquake".
### diff.py
Run `diff.py` with the output of `poll-twitter.py` piped to it. More explicitly, run `poll-twitter.py | diff.py`.
The output of this file is the time difference of each streamed tweet, together with its own time stamp. We took the output of `poll-tweepy.py` and calculate the time difference of each streamed data.
### insert.py
Run `insert.py` with the output of `diff.py` piped to it. More explicitly, run `poll-twitter.py | diff.py | insert.py`.
The purpose of this file is to insert the result of `diff.py` to redis database. We set the time stamp as the key, and the time difference as the value associated with the key, and then store them in the redis database.
### avg.py
Run `avg.py` with the output of `insert.py` piped to it. More explicitly, run `poll-twitter.py | diff.py | insert.py` | avg.py.
We are calculating rate of twitter stream in this file, by reading from redis database. The rate can be calculated in this way:
```rate = sum(time difference) / number of records```
Where time difference is the value stored in the redis database. `number of records` would go up by time, and drop down when it reaches expiration time we set in `insert.py` file.