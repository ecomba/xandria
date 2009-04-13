from google.appengine.ext import db
from google.appengine.ext import webapp

class Feed(db.Model):
  url = db.StringProperty()
  
  def save(self):
    self.put()
  
  @staticmethod  
  def findAll():
    return Feed.all().fetch(limit = 1000)

class FeedsPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Welcome to Aggregator')

    feeds = Feed.findAll()
    for feed in feeds:
      self.response.out.write(feed.url)
  