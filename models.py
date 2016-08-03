'''
Models.py

This file contains all the data models to be used in the main application
Uses the datastore non-relational database of Google App Engine.
'''

from google.appengine.api import users
from google.appengine.ext import ndb

class GvUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=False)
    last_name = ndb.StringProperty(required=False)
    lastknown_latitude = ndb.FloatProperty(required=False)
    lastknown_longitude = ndb.FloatProperty(required=False)
    
class Meetup(ndb.Model):
    name = ndb.StringProperty(required=True)
    event_admin = ndb.StringProperty(required=False)
    guest1 = ndb.StringProperty(required=True)
    guest2 = ndb.StringProperty(required=False)
    guest3 = ndb.StringProperty(required=False)
    guest4 = ndb.StringProperty(required=False)
    guest5 = ndb.StringProperty(required=False)
    type_of_places = ndb.StringProperty(required=True)
    recommendation_map = ndb.StringProperty(required=False)
    recommendation_list = ndb.StringProperty(required=False)
