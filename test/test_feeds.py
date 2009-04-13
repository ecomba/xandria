import unittest
from feeds import Feed

class FeedTest(unittest.TestCase):
  def setUp(self):
    self.url = 'url'
    self.feed = Feed(url = self.url)

  def testShouldExist(self):
    try:
      Feed(url = None)
    except NameError, e:
      self.fail(str(e) + 'The Feeds class does not exist! What are you waiting for?')
      
  def testFeedShouldHaveUrl(self):
    self.assertEquals(self.url, self.feed.url)
    
  def testShouldProvideEmptyListIfNoFeedsExist(self):
    self.assertEquals([], Feed.findAll())
    
  def testShouldSaveAFeedAndReturnAListWithOneFeedOnly(self):
    self.feed.save()
    self.assertEquals(1, len(Feed.findAll()))
  
  def testShouldSaveMoreThanOneFeedAndReturnThem(self):
    self.feed.save()
    Feed(url='some.other.url').save()
    self.assertEquals(2, len(Feed.findAll()))