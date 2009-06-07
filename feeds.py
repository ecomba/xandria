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
    error = None
    if self.request.get("error") == 'no_url':
      error = 'No url provided!'
      
    template_values = {
      "error" : error,
      "feeds" : Feed.findAll()
    }
    
    path = os.path.join(os.path.dirname(__file__), "html/feeds.html")
    self.response.out.write(template.render(path, template_values))

  def post(self):
    url = self.request.get("url")
    if url == '':
      self.redirect("/feeds?error=no_url")
    else:
      feed = Feed(url = url)
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

  def post(self):
    method = self.request.get("_method")
    if method == "delete":
      path = self.request.path
      Feed.find(path.replace('/feeds/', '')).delete()
      self.redirect("/feeds")
    pass