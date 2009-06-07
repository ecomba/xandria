from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from feeds import FeedHandler
from feeds import FeedsHandler

application = webapp.WSGIApplication([('^/feeds/?$', FeedsHandler),
                                      ('/feeds/.*', FeedHandler)], debug=True)

def main():
  run_wsgi_app(application)
  
if __name__ == "__main__":
  main()
