from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Visitors(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_html = jinja_environment.get_template('Templates/login.html')
        self.response.write(login_html.render())

    def post(self):
        visitor = Visitors(name=self.request.get('name'), email=self.request.get('email'), username=self.request.get("username"), password=self.request.get('password'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("HELLO IM WORKING")

app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/order', MainHandler),
], debug=True)
