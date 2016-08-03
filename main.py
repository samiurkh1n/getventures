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
from models import GvUser
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
        app_user = users.get_current_user()
        # Check to see if user logged in
        if user:
            self.greeting = ('Welcome, %s (<a href="%s">Sign out</a>)') %(user.nickname(), users.create_logout_url('/'))
        else:
            self.greeting = ('<a href="%s">Sign in or register</a>') %users.create_login_url('/')
        return self.greeting

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
        self.response.write(template.render())
 
    def post(self):
        '''
        Executes when the HTTP POST/ request is received. 
        Specifically, when the user clicks on the "Plan meetup" button.
        Input is the POST request. User query string is stored via jinja variables. 
        '''
        # Executes with POST/. Specifically, when the user clicks on the "Plan meetup" button.
        # Does not allow it if user not logged in.
        user = users.get_current_user()
        if user:
        # add an if branch here to test if the user's first name is the database, in which case if it isn't redirect to account
            app_user = GvUser.get_by_id(users.user_id())
            if app_user:
                loggedin_alert = '<script> alert("Welcome back!"); </script>'
                self.response.write('%s' %loggedin_alert)  
                self.redirect('/event')
            else:
                self.redirect('/account')
        else:
            template = jinja_environment.get_template('templates/main.html')
            warning = '<script> alert("Please login."); </script>'
            self.response.write('%s' %warning)
            greeting = self.check_login()
            self.response.write("%s" %greeting)
            self.response.write(template.render())
        

class AccountHandler(webapp2.RequestHandler):
    '''
    AccountHandler allows account holders to include information like first and last name.
    This handler should execute if and only if the user has no first name and last name in the datastore. 
    '''

    # TODO - get user id, check if the user id exists, then just retrieve user, otherwise retrieve new user
    def get(self):
        '''
        Executes with GET /account. 
        Input is a GET request.
        Output is the rendering of account.html located in the templates folder.
        User.html is a form to add first and last name and should only execute if user first name and last name isn't stored already.
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
        user = users.get_current_user()
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        user_email = self.request.get('email')
        current_user = GvUser(email=user_email,first_name=firstname,last_name=lastname,id=user.user_id())
        current_user.put()
        
        self.redirect('/event') 

class EventHandler(webapp2.RequestHandler):
    def get(self):
        ''' 
        Executes when GET /event is received. 
        Input is the GET /event request.
        Output is a rendering of the input.html file
        '''
        template = jinja_environment.get_template('templates/input.html')
        # Get location script should be triggered here and store location in datastore
        self.response.write(template.render())
        
    def post(self):
        #THE MOST SIGNIFICANT FUNCTION ON THIS WEBSITE
        '''
        Executes when POST/event is received.
        Input is the user query attached to variables and other user data (ex: location in lat and long)
        Output is the map and list and the subsequent storage into an object of type Event (ndb model). 
        '''
        template = jinja_environment.get_template('templates/output.html')
        self.response.write(template.render())

        #User input stored as variables
        session_name = self.request.get('session_name')
        session_guest1 = self.request.get('session_guest1')
        session_guest2 = self.request.get('session_guest2')
        session_guest3 = self.request.get('session_guest3')
        session_guest4 = self.request.get('session_guest4')
        session_guest5 = self.request.get('session_guest5')
        place_type = self.request.get('place_type') 

        #display output map
        output_map = self.response.write("map here")
        self.response.write(output_map) 

        #send data to datastore
        current_session = Meetup(name=session_name,event_admin="samiurkh1n@gmail.com",guest1=session_guest1,guest2=session_guest2,guest3=session_guest3,guest4=session_guest4,guest5=session_guest5,type_of_places=place_type)
        current_session.put()
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/account', AccountHandler),
    ('/event' , EventHandler),
], debug=True)
