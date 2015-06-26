# STEP 002
# This is a dummy model that your MapReduce job wil iterate over

from google.appengine.ext import ndb

class Dummy(ndb.Model):
	counter = ndb.IntegerProperty(default=0)