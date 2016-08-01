from google.appengine.api import users
import jinja2
import os
import webapp2
import models
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      email_address = user.nickname()
      user_input = models.User.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">Sign out</a>' % (

          users.create_logout_url('/'))
      if user_input:
        home_html = jinja_environment.get_template('Templates/home.html')
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              user_input.first_name,
              user_input.last_name,
              email_address,
              signout_link_html))
        self.response.write(home_html.render())
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
    home_html = jinja_environment.get_template('Templates/home.html')
    user = users.get_current_user()
    if not user:
      self.error(500)
      return
    user_input = models.User(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        id=user.user_id())
    user_input.put()
    self.response.write('Thanks for signing up, %s!' %
        user_input.first_name)
    self.response.write(home_html.render())

class AccompHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/accomp.html')
        self.response.write(template.render())


    def post(self):
        template = jinja_environment.get_template('templates/thank_you.html')
        accomp_info = {
            'feeling_answer': self.request.get('feeling'),
            'accomp_info_answer': self.request.get('accomp_text')
        }
        accomp_info_record = models.Accomplishments(
            feeling = accomp_info['feeling_answer'],
            accomp_info = accomp_info['accomp_info_answer'],
        )
        accomp_info_record.put()
        self.response.write(template.render())



class AccompHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/accomp.html')
        self.response.write(template.render())


    def post(self):
        template = jinja_environment.get_template('templates/thank_you.html')
        accomp_info = {
            'feeling_answer': self.request.get('feeling'),
            'accomp_info_answer': self.request.get('accomp_text')
        }
        accomp_info_record = models.Accomplishments(
            feeling = accomp_info['feeling_answer'],
            accomp_info = accomp_info['accomp_info_answer'],
        )
        accomp_info_record.put()
        self.response.write(template.render())



app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/accomp', AccompHandler)
], debug=True)
