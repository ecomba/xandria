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

class FeedsHandler(webapp.RequestHandler):
  def get(self):
    feeds = Feed.findAll()
    template_values = {
      "feeds" : feeds 
    }
    
    path = os.path.join(os.path.dirname(__file__), "html/feeds.html")
    self.response.out.write(template.render(path, template_values))

  def post(self):
    feed = Feed(url = self.request.get("url"))
    feed.save()
    
    self.redirect("/feeds")