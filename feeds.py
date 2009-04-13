from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class FeedsPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Welcome to Aggregator')

    # feeds = Feed.findAll()
    # for feed in feeds:
    #   self.response.out.write(feed.url)
    

application = webapp.WSGIApplication([('/feeds', FeedsPage)], debug=True)

def main():
  run_wsgi_app(application)
  
if __name__ == "__main__":
  main()
  
class Feed(db.Model):
  url = db.StringProperty()
  
  def save(self):
    self.put()
  
  @staticmethod  
  def findAll():
    return Feed.all().fetch(limit = 1000)
    
    