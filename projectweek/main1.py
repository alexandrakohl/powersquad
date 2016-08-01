from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

class User(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      email_address = user.nickname()
      user_input = User.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      if user_input:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              user_input.first_name,
              user_input.last_name,
              email_address,
              signout_link_html))
      else:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <input type="text" name="first_name">
            <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))

  def post(self):
    user = users.get_current_user()
    if not user:
      self.error(500)
      return
    user_input = User(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        id=user.user_id())
    user_input.put()
    self.response.write('Thanks for signing up, %s!' %
        user_input.first_name)

app = webapp2.WSGIApplication([
  ('/', LoginHandler)
], debug=True)
