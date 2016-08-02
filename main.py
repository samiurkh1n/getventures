#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.api import users
from models import User
from models import Meetup

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

### VERY IMPORTANT TODO - discuss with Emma how variables are being sent around.

class MainHandler(webapp2.RequestHandler):
    # Main home page (main.html) 
    
    def check_login(self):
        '''
        Method that checks if the user is logged in (within the MainHandler object).
        Input originates from the User API. The user variable stores the user email.
        Output is a set of text displaying the login status. 
        '''
        user = users.get_current_user()
        # Check to see if user logged in
        if user:
            self.greeting = ('Welcome, %s (<a href="%s">Sign out</a>)') %(user.nickname(), users.create_logout_url('/'))
        else:
            self.greeting = ('<a href="%s">Sign in or register</a>') %users.create_login_url('/account')
        return self.greeting

    def alert_user_of_login(self):
        user = users.get_current_user()
        # Warns user that they need to log in, else it breaks the function
        if user:
            pass
        else:
            self.warning = ('<script> alert("Please login."); </script>')
        return self.warning
    
    def get(self):
        '''
        Executes when the GET / HTTP request is received.
        Input is the GET request. 
        Output is the rendering of main.html file located in templates folder.
        '''
        template = jinja_environment.get_template('templates/main.html')
        # Greeting is a test of whether the user logged-in.
        greeting = self.check_login()
        self.response.write("%s" %greeting)
        # Main.html contains a button to plan event that redirects an GET request to EventHandler ('/event')
        self.response.write(template.render())
 
    def post(self):
        '''
        Executes when the HTTP POST/ request is received. 
        Specifically, when the user clicks on the "Plan meetup" button.
        Input is the POST request. User query string is stored via jinja variables. 
        // TODO: Consult Emma on variable names
        '''
        # Executes with POST/. Specifically, when the user clicks on the "Plan meetup" button.
        # Does not allow it if user not logged in.
        warning = self.alert_user_of_login()
        self.response.write("%s" %warning)
        self.redirect('/event') 
        

class AccountHandler(webapp2.RequestHandler):

    def get(self):
        '''
        Executes with GET /account. 
        Input is a GET request.
        Output is the rendering of account.html located in the templates folder.
        '''
        template = jinja_environment.get_template('templates/user.html')
        self.response.write(template.render())
        
    def post(self):
        '''
        Executes with the POST /account. User adds account information this way.
        Input is a POST request.  User query string is stored via jinja variables. 
        // TODO: Consult Emma on variable names
        Output should 
        1. Redisplay user inputs
        2. Store user input into User data store.
        '''
        # variable names firstname, lastname, lastknownlong, lastknownlat
        current_user = User(email=users.get_current_user(),first_name=firstname,lastknown_latitude=lastknownlong,lastknown_longitude=lastknownlat) 

class EventHandler(webapp2.RequestHandler):
    def get(self):
        ''' 
        Executes when GET /event is received. 
        Input is the GET /event request.
        Output is a rendering of the input.html file
        '''
        template = jinja_environment.get_template('templates/input.html')
        self.response.write(template.render())
        
    def post(self):
        #THE MOST SIGNIFICANT FUNCTION ON THIS WEBSITE
        '''
        Executes when POST/event is received.
        Input is the user query attached to variables and other user data (ex: location in lat and long)
        Output is the map and list and the subsequent storage into an object of type Event (ndb model). 
        '''
        template = jinja_environment.get_template('templates/output.html')
        #compute here
        self.response.write(template.render())
        # jinja variables are session_name, session_description, session_guests, place_type, map_output, list_output
        current_session = Meetup(name=session_name,description=session_description,event_admin=users.get_current_user(),event_participants=session_guests,type_of_places=place_type,recommendation_map=map_output,recommendation_list=list_output)
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/account', AccountHandler),
    ('/event' , EventHandler),
], debug=True)
