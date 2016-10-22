# twitterconversations

A simple library to retreive twitter conversations for research use. It works by gettings lots of tweets through Twitter's Streaming API. Then for each tweet that replied to something else, it gets that reply, and repeats up the chain. This is a simple (imperfect) way to get conversational twitter data.

This uses code slightly modified from [https://github.com/geduldig/TwitterAPI](https://github.com/geduldig/TwitterAPI)

Example Usage:

```python
from twitterconversations import twitterconversations

getter = twitterconversations.TwitterConversations(consumer_key, consumer_secret, access_token_key, access_token_secret)

tweets = getter.getStatuses(100) # If this doesn't print anything after about 10 seconds (it should print 1, then 2, then 3, then ...) kill it and run it again

replies = getter.getReplies(tweets, 10) # Goes up the reply chain a maximum of 10 times, so any conversation you have will be 10 tweets or less

replies.sort(key=lambda x: -len(x)) # sort the reply chains so the longest ones are first

# now replies[0] will be an array of tweets, where replies[0][i] has replies[0][i+1] as a response
```
