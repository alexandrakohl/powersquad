from google.appengine.api import users
import jinja2
import os
import webapp2
from google.appengine.ext import ndb

class CoolUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    feeling = ndb.StringProperty()

class Accomplishments(ndb.Model):
    accomp_info = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.DateTimeProperty(auto_now_add = True)
    email = ndb.StringProperty()

class Compliments(ndb.Model):
    comp_info = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    email = ndb.StringProperty()

class Journal(ndb.Model):
    journal_entry = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add=True)
    email = ndb.StringProperty()
    #time??"""
