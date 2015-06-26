import webapp2
import logging

from dummy import Dummy
from mapreduce import control

# This handler populates your Datastore with Dummy objects. You access it by going to:
# http://yourapp.appspot.com/populate_db
#
# By default it will create 100 entities of the Dummy object in the Datastore, but you can provide an additional ?count= param to override it like this:
# http://yourapp.appspot.com/populate_db?count=200
# in order to put in more of those.
#
class PopulateHandler(webapp2.RequestHandler):
	def get(self):
		count = 100
		if self.request.get('count'):
			count =  int(self.request.get('count'))

		for i in range(0, count):
			d = Dummy()
			d.put()


# the magic happens here
class StartHandler(webapp2.RequestHandler):
	def get(self):
		processing_rate = 3
		shard_count = 2

		control.start_map(
			"Iterate over all Dummy objects in the DB",     #this an arbitrary description string
			"tasks.mapper_function",                        #this is the function that will bne
			"mapreduce.input_readers.DatastoreInputReader",
			{
				"entity_kind": "dummy.Dummy",               #the model that you will iterate over
				"processing_rate": processing_rate,         #how many entities will each shard process
			},
			shard_count=shard_count,                        #how many shards will be created by every MR controller
			queue_name="default",                           #the name of the queue that will be used for this MR's jobs, I used default to minimize config
		)

def mapper_function(dummy):
	dummy.counter += 1
	dummy.put()
	logging.info("Dummy entry with id: {}, new counter value: {}".format(dummy.key.id(), dummy.counter))

app = webapp2.WSGIApplication([
	('/populate_db', PopulateHandler),
	('/start_job', StartHandler),
], debug=True)

