'''
Models.py

This file contains all the data models to be used in the main application
Uses the datastore non-relational database of Google App Engine.
'''

from google.appengine.api import users
from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=False)
    last_name = ndb.StringProperty(required=False)
    lastknown_latitude = ndb.FloatProperty(required=True)
    lastknown_longitude = ndb.FloatProperty(required=True)
    
class Meetup(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=False)
    event_admin = ndb.StringProperty(required=True)
    event_participants = ndb.StringProperty(required=True)
    type_of_places = ndb.StringProperty(required=True)
    recommendation_map = ndb.StringProperty(required=False)
    recommendation_list = ndb.StringProperty(required=False)
