from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

class CoolUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
class Accomplishments(ndb.Model):
    feeling = ndb.StringProperty()
    accomp_info = ndb.StringProperty()
    user = ndb.KeyProperty(kind = CoolUser) #allows us grab all of the properties
class Compliments(ndb.Model):
    comp_info = ndb.StringProperty()
    user = ndb.KeyProperty(kind = CoolUser)
class Journal(ndb.Model):
    """
    journal_entry = ndb.StringProperty()
    #time??"""
