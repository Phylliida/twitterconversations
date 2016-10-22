import time
import re
from TwitterAPI import TwitterAPI


class TwitterConversations:
  def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
    self.api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    
                        
  def getStatuses(self, n, filterData=None, debug=True):
    if filterData is None:
      filterData = {'locations':'-74,40,-73,41', "languages": "en"}
    r = self.api.request('statuses/filter', filterData)
    statuses = []
    for i, status in enumerate(r):
      statuses.append(status)
      if debug: print i
      if i == n-1: break
    return statuses

  def getReplies(self, statuses, depth):
    replies = self.getRepliesHelper(statuses, depth, set())
    
    replyChains = []
    replyMap = {}
    
    for reply in replies:
      replyMap[reply['id_str']] = reply
    
    for status in statuses:
      if status['id_str'] in replyMap: continue # we are looking at a child of this comment somewhere else
      curChain = [status]
      curStatus = status
      while not curStatus['in_reply_to_status_id_str'] is None:
        inReplyToId = curStatus['in_reply_to_status_id_str']
        if not inReplyToId in replyMap: break
        curStatus = replyMap[inReplyToId]
        curChain.append(curStatus)
      replyChains.append(curChain[::-1])
    
    return replyChains

  def getRepliesHelper(self, statuses, depth, gotSoFar):
    replyIds = []
    for status in statuses:
      replyId = status['in_reply_to_status_id_str']
      if not replyId is None and not replyId in gotSoFar:
        replyIds.append(replyId)
        gotSoFar.add(replyId)

      
    replies = []
    while True:
      replyBatch = replyIds[:100]
      replyIds = replyIds[100:]
      if len(replyBatch) == 0: break
      replies += [thing for thing in self.api.request('statuses/lookup', {'id': ",".join(replyBatch)})]

    if len(replies) > 0 and depth > 1:
      replies += self.getRepliesHelper(replies, depth-1, gotSoFar)
    
    
    return replies

  def parseTweet(self, tweet):
    return "-" + tweet['user']['screen_name'] + ": " + tweet['text']
    
  # If you want this can get tweet conversations in the form of:
  # -user1: words said
  # -user2: words said
  # -user1: words said
  # etc.
  def parseReplyChains(self, replyChains):
    replyChainTexts = []
    
    replyChains.sort(key=lambda x: -len(x))
    
    for replyChain in replyChains:
      if len(replyChain) == 1: continue
      replyChainTexts.append(re.sub("@\w+ ", "", "\n".join([self.parseTweet(tweet) for tweet in replyChain])))
    
    return replyChainTexts

  # To save these you will want to do 
  
  # import codecs
  # f = codecs.open(path, "wb", "utf-8-sig")
  # (stuff as normal)
  # f.close()
  
  # Otherwise you will get encoding issues
