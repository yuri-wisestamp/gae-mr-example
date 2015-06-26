import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Map Reduce over App Engine example')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
