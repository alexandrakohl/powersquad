from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_html = jinja_environment.get_template('Templates/login.html')
        self.response.write(login_html.render())

    def post(self):
        login_output = jinja_environment.get_template('Templates/output_login.html')
        user_info = {
            'name_answer': self.request.get('name'),
            'email_answer': self.request.get('email'),
            'username_answer': self.request.get('username_signin'),
            'password_answer': self.request.get('password')
        }

        user_record = User(
            name= user_info['name_answer'],
            email= user_info['email_answer'],
            username= user_info['username_answer'],
            password= user_info['password_answer']
        )
        user_record.put()
        self.response.write(login_output.render(user_info))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("HELLO IM WORKING")

app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/home', MainHandler),
], debug=True)
