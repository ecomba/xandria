from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class Feed(db.Model):
  url = db.StringProperty()
  
  def save(self):
    self.put()
  
  @staticmethod  
  def findAll():
    return Feed.all().fetch(limit = 1000)
    
  @staticmethod
  def find(searchedUrl):
    resultFeed = None
    try:
      resultFeed = db.GqlQuery("SELECT * FROM Feed WHERE url = :url", url = searchedUrl).fetch(1)[0]
    except IndexError:
      pass

    return resultFeed
    
class FeedsHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
      "feeds" : Feed.findAll()
    }
    
    path = os.path.join(os.path.dirname(__file__), "html/feeds.html")
    self.response.out.write(template.render(path, template_values))

  def post(self):
    feed = Feed(url = self.request.get("url"))
    feed.save()
    
    self.redirect("/feeds")
    
class FeedHandler(webapp.RequestHandler):
  """Handles the requestst to a single Feed"""
  def get(self):
    path = self.request.path
    template_values = {
      "feed" : Feed.find(path.replace('/feeds/', ''))
    }
    
    path = os.path.join(os.path.dirname(__file__), "html/feed.html")
    self.response.out.write(template.render(path, template_values))
  