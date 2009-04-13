import unittest
from feeds import Feed

class FeedTest(unittest.TestCase):
  def test_should_exist(self):
    """Is the class there?"""
    try:
      Feed()
    except NameError, e:
      self.fail(str(e) + 'The Feeds class does not exist! What are you waiting for?')