from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
class Accomplishments(ndb.Model):
    feeling = ndb.StringProperty()
    accomp_info = ndb.StringProperty()
    user = ndb.KeyProperty() #allows us grab all of the properties
