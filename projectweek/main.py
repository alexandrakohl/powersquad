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
        print "WOOHOO"
        user = users.get_current_user()
        login_url_template = jinja_environment.get_template('Templates/login1.html')
        if user:
          email_address = user.nickname()
          user_input = User.get_by_id(user.user_id())
          signin_link_html = (users.create_logout_url('/'))
          print "IF"
          if user_input:
             self.response.write("Welcome")
        else:
            print "ELSE"
            self.response.write(login_url_template.render({'login_url': users.create_login_url}))

    def post(self):
        login_output = jinja_environment.get_template('Templates/output_login.html')
        user = users.get_current_user()
        if not user:
            self.error(500)
            return

        user_info = {
           'name_answer': self.request.get('name'),
           'username_answer': self.request.get('username_signin'),
        }
        user_input = User(
            name=self.request.get('name'),
            username=self.request.get('username_signin'),
            id=user.user_id())
        user_input.put()
        self.response.write('Thanks for signing up')
        self.response.write(login_output.render(user_info))



class MainHandler(webapp2.RequestHandler):
   def get(self):
       self.response.write("HELLO IM WORKING")

app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/home', MainHandler),
], debug=True)
