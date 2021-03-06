import unittest
from webtest import TestApp
from google.appengine.ext import webapp
from feeds import Feed
from feeds import FeedsHandler
from feeds import FeedHandler

class FeedUnitTest(unittest.TestCase):
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
  
  def testShouldDeleteAnEntry(self):
    self.feed.save()
    self.assertEquals(1, len(Feed.findAll()))
    self.feed.delete()
    self.assertEquals(0, len(Feed.findAll()))

  def testShouldFindOneFeed(self):
    self.feed.save()
    Feed(url='example.com').save()
    self.assertEquals('example.com', Feed.find('example.com').url)
    
  def testShouldReturnNoneWhenThereIsNothingToBeFound(self):
    self.assertEquals(None, Feed.find('somthing'))

class FeedsHandlerTest(unittest.TestCase):
  def setUp(self):
    self.application = webapp.WSGIApplication([('^/feeds/?$', FeedsHandler),
                                               ('/feeds/.*', FeedHandler)], debug=True)

  def assertContains(self, itemToLookFor, itemToSearch):
    def escapeHtml(string):
      return string.replace("<", "&lt;")
    
    escapedItemToLookFor = escapeHtml(itemToLookFor)
    escapedItemToSearch = escapeHtml(str(itemToSearch))
    self.assertTrue(itemToLookFor in itemToSearch, "%s did not contain %s" % (escapedItemToSearch, escapedItemToLookFor))

  def testShouldBeStatus200(self):
    app = TestApp(self.application)
    response = app.get('/feeds')
    self.assertEquals('200 OK', response.status)
    
  def testShouldHaveAForm(self):
    app = TestApp(self.application)
    response = app.get('/feeds')
    self.assertContains('<form method="post">', response)
    self.assertContains('<input type="text" name="url"/>', response)

  def testShouldAddFeedToList(self):
    app = TestApp(self.application)
    postResponse = app.post('/feeds?url=example.com')
    response = postResponse.follow()
    self.assertContains('<li><a href="/feeds/example.com">example.com</a>', response)

  def testShouldNotAllowAnEmptyUrl(self):
    app = TestApp(self.application)
    postResponse = app.post('/feeds?url=')
    response = postResponse.follow()
    self.assertContains('No url provided!', response)
    
class FeedHanderTest(unittest.TestCase):
  def setUp(self):
    self.application = webapp.WSGIApplication([('^/feeds/?$', FeedsHandler),
                                               ('/feeds/.*', FeedHandler)], debug=True)

  def testShouldBeStatus200(self):
    app = TestApp(self.application)
    feed = Feed(url = 'example.com')
    feed.save
    response = app.get("/feeds/example.com")
    self.assertEquals('200 OK', response.status)
    
  def testShouldDisplayTheFeed(self):
    app = TestApp(self.application)
    feed = Feed(url = 'example.com')
    feed.save()
    
    response = app.get("/feeds/example.com")
    self.assertTrue('<h1>example.com</h1>' in response)
    
  def testShouldDeleteAFeed(self):
    app = TestApp(self.application)
    addFeed = app.post('/feeds?url=example.com')
    deleteResponse = app.post('/feeds/example.com?_method=delete')
    response = deleteResponse.follow()
    self.assertFalse('example.com' in response)
    
