from google.appengine.ext import db

class Feed(db.Model):
  url = db.StringProperty()
  
  def save(self):
    self.put()
  
  @staticmethod  
  def findAll():
    return Feed.all().fetch(limit = 1000)
    
    