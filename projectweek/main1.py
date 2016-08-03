from google.appengine.api import users
import jinja2
import os
import webapp2
import models
from google.appengine.ext import ndb
import random
import logging

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

cool_user_id = ""

compliment_template = {
    'random_compliment_0' : 'You are so rad!',
    'random_compliment_1' : 'You hair looks nice today!',
    'random_compliment_2' : 'Nice outfit!',
    'random_compliment_3' : 'You got a nice butt buddy!',
    'random_compliment_4' : 'You matter',
    }

logging.info(compliment_template)
random_compliment = random.choice(compliment_template.values())
logging.info(random_compliment)
compliment_template_1 = {
  'random_compliment' : random_compliment,
}

class LoginHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      email_address = user.nickname()
      user_input = models.CoolUser.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">Sign out</a>' % (users.create_logout_url('/'))
      if user_input:
        home_html = jinja_environment.get_template('Templates/home.html')

        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              user_input.first_name,
              user_input.last_name,
              email_address,
              signout_link_html))
        self.response.write(home_html.render(compliment_template_1))

      else:
        register_html = jinja_environment.get_template('Templates/login.html')
        self.response.write(register_html.render())

    else:
        login_link_html = users.create_login_url('/')
        login_dictionary = {'login_link_html':login_link_html}
        login_html = jinja_environment.get_template('Templates/login1.html')
        self.response.write(login_html.render(login_dictionary))

  def post(self):
    home_html = jinja_environment.get_template('Templates/home.html')
    app_user = users.get_current_user()
#    app_user.user_id() #using the app API, I am accessing the user id
    rating_info = self.request.get('rating') #CHECK IF THIS WORKS AT HOME
    if not app_user:
      self.error(500)
      return
    user_input = models.CoolUser(
        first_name = self.request.get('first_name'),
        last_name = self.request.get('last_name'),
        email = app_user.email(),
        feeling = self.request.get('feeling'), #CHECK IF IT IS STORE AS AN INT OR AS A STRING
        id = app_user.user_id())

    user_input.put()
    #cool_user_key = user_input.put()
    cool_user_id = models.CoolUser.get_by_id(app_user.user_id()) #sets it so that for that same
    #user, there will only be one unique ID
    self.response.write(app_user.user_id())
    self.response.write(cool_user_id)
    self.response.write('Thanks for signing up, %s!' %
        user_input.first_name)
    self.response.write(home_html.render(compliment_template_1))

class AccompHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('Templates/accomp.html')
        self.response.write(template.render())


    def post(self):
        app_user = users.get_current_user()
        cool_user_id = app_user.user_id() #using the app API, I am accessing the user id

        template = jinja_environment.get_template('Templates/thank_you.html')
        accomp_info_answer = {
            "text": self.request.get('accomp_text'),
            "email": app_user.email(),
#            "personal_accomp":
            "email": app_user.email(),
            }
        accomp_info_record = models.Accomplishments(
            accomp_info = accomp_info_answer["text"],
            email = accomp_info_answer["email"]
            )
        app_user_query = models.Accomplishments.all().filter(app_user.email() == accomp_info_answer["email"])
        accomplishment_data = app_user_query.fetch()

        for data in accomplishment_data:
            self.response.out.write('<p>'+data.accomp_info+'</p>')

        accomp_info_record.put()
        self.response.write(template.render(accomp_info_answer))

class CompHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('Templates/comp.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('Templates/thank_you.html')
        comp_info = {
            'comp_text_answer': self.request.get('comp_text')
        }
        comp_info_record = models.Compliments(
            comp = comp_info['comp_text_answer'],
            #user = cool_user_id
        )
        comp_info_record.put()
        self.response.write(template.render())

class JournalHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('Templates/journal.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('Templates/thank_you.html')
        comp_info = {
            'comp_text_answer': self.request.get('comp_text')
        }
        comp_info_record = models.Compliments(
            comp = comp_info['comp_text_answer'],
        )
        comp_info_record.put()
        self.response.write(template.render())

class AccompLibraryHandler(webapp2.RequestHandler):
    def get(self):
        template1 = jinja_environment.get_template('Templates/accomplibrary.html')
        self.response.write(template1.render())

class CompLibraryHandler(webapp2.RequestHandler):
    def get(self):
        template1 = jinja_environment.get_template('Templates/complibrary.html')
        self.response.write(template1.render())

app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/accomp', AccompHandler),
  ('/comp', CompHandler),
  ('/journal', JournalHandler),
  ('/accomplibrary', AccompLibraryHandler),
  ('/complibrary', CompLibraryHandler)
], debug=True)
