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

    def post_accomp(self):
        value = self.request.body #getting the entire body of the reuest which was sent as a second argument in the $ post method in JS
        print "value: " + value
        time.sleep(10)
        self.response.write('POSTED! ' + value)

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
        accomp_info_record.put()

        accomplishments_query = models.Accomplishments.query()
        accomplishments_query = accomplishments_query.filter(models.Accomplishments.email == accomp_info_answer["email"])
        accomplishment_data = accomplishments_query.fetch()

        for data in accomplishment_data:
            self.response.out.write('<p>'+data.accomp_info+'</p>')

        self.response.write(template.render(accomp_info_answer))

class AccompLibraryHandler(webapp2.RequestHandler):
    def get(self):
        app_user = users.get_current_user()
        template1 = jinja_environment.get_template('Templates/accomplibrary.html')
        accomp_info_answer = {
            'email': app_user.email(),
            'text': self.request.get('accomp_info'),
            }
        accomp_info_record = models.Accomplishments(
            email = accomp_info_answer['email'],
            accomp_info = accomp_info_answer['text'],
            )
        accomp_store = models.Accomplishments.query().filter(models.Accomplishments.email==accomp_info_answer['email'])

        accomplishment_data = accomp_store.fetch()
        accomp_store_dict ={}
        for i, instance in enumerate(accomplishment_data):
            accomp_store_dict['random_key_%d' % i] = instance
        logging.info (accomp_store_dict)

        self.response.write(template1.render(accomp_store_dict=accomp_store_dict))


class CompHandler(webapp2.RequestHandler):
    def get(self):
        app_user = users.get_current_user()
        template2 = jinja_environment.get_template('Templates/comp.html')
        self.response.write(template2.render())

    def post(self):
        template = jinja_environment.get_template('Templates/thank_you.html')
        comp_info = {
            'email': app_user.email(),
            'comp_text_answer': self.request.get('comp_text')
        }
        comp_info_record = models.Compliments(
            email = comp_info_answer['email'],
            comp_info = comp_info['comp_text_answer']
            #user = cool_user_id
        )
        comp_info_record.put()
        compliments_query = models.Compliments.query()
        compliments_query = compliments_query.filter(models.Compliments.email == comp_info_answer['email'])
        Compliments_data = accomplishments_query.fetch()

        for data in compliment_data:
            self.response.out.write('<p>'+data.comp_info+'</p>')

        self.response.write(template2.render())

class JournalHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('Templates/journal.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('Templates/thank_you.html')
        journal_info = {
            'comp_text_answer': self.request.get('journal_text')
        }
        journal_info_record = models.Compliments(
            journal = journal_info['journal_text_answer'],
        )
        journal_info_record.put()
        journal_query = models.Journal.query()
        journal_query = journal_query.filter(models.Compliments.email == accomp_info_answer["email"]) #INCLUDES EVERYTHING
        #BUT THE ENTRY JUST ENTERED!! SO ENTER THE JUST ENTERED ENTRY MANUALLY
        #this actually might not be a problem because we are NOT displaying the accomplishments on that same page (in the library)
        Journal_data = journal_query.fetch()
        self.response.write(template.render())


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
