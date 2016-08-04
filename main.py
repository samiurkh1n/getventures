'''
Getevent by Emma Davitz, Daryll Henry, Samiur Khan, Riccardo Crepreci, Christophe Q., Chris,

What is this app about?
An app that allows you to hangout spots for you and your friends that are equidistant from every person.

Purpose of this file:
This is the handler file, where user HTTP requests (usually either GET and POST) are redirected to different classes to execute.
'''
import webapp2
import jinja2
import os
from google.appengine.api import users
from models import GvUser
from models import Meetup

#Every html file is rendered with the jinja library.
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__))) 

class MainHandler(webapp2.RequestHandler):
    '''
    This is the home page (the first page that a user request would render.
    This page is a gateway to the application. 
    From the user perspective, either a user can create an account or, if they already have an account, they are forwarded to a page that
    allows them to plan events.
    From the server perspective, this handler allows us to store app-critical information about users and their location.
    In this handler, we check if the user has an account or not. The website is restricted unless they create an account.
    When the user logs in, we store key info like their email, user_id (from the User API), and their last known lat and long.
    Their last known lat and long is used in the main application to track location and offer better recommendations for where they should hangout.
    '''
    
    def check_login(self):
        '''
        Method that checks if the user is logged in (within the MainHandler object).
        Input originates from the User API. The user variable stores the user email.
        Output is a set of text displaying the login status and the execution of the script that gets location (does not store it).  
        '''
        #Checks user datastore and assign the user with app_user
        #If user does exist, we display text welcoming, them and offer to sign off. We also execute the script to attain their location.
        #If the user does not exist (they aren't logged in), we ask them to login and do not execute the script to attain location.
        app_user = users.get_current_user()
        if app_user:
            self.greeting = ('Welcome, %s (<a href="%s">Sign out</a>)') %(app_user.nickname(), users.create_logout_url('/'))
            # TODO - have location determining script execute here, but how?
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
        # Greeting is a test of whether the user logged-in. Referenced above.
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
        # Does not allow redirect to /event if user not logged in.
        user = users.get_current_user()
        template = jinja_environment.get_template('templates/main.html')
        self.response.write(template.render())
        if user:
            # Attain and store the user's last known location
            app_user = GvUser.get_by_id(user.user_id())
           
            if app_user:
                latitude = self.request.get('lat')
                longitude = self.request.get('long')
                app_user.lastknown_latitude = latitude
                app_user.lastknown_longitude = longitude
                app_user.put()
                self.redirect('/event')
            else:
                #If the user does not exist in GvUser datastore, we redirect them to account handler
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
        Output should 
        1. Redisplay user inputs
        2. Store user input into User data store.
        '''
        app_user = users.get_current_user()

        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        user_email = app_user.email()
        latitude = self.request.get('lat')
        longitude = self.request.get('long')

        current_user = GvUser(email=user_email,
                              first_name=firstname,
                              last_name=lastname,
                              id=app_user.user_id(),
                              lastknown_latitude=latitude,
                              lastknown_longitude=longitude)
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
        app_user = users.get_current_user()

        #User input stored as variables
        session_name = self.request.get('session_name')
        session_guest1 = self.request.get('session_guest1')
        session_guest2 = self.request.get('session_guest2')
        session_guest3 = self.request.get('session_guest3')
        session_guest4 = self.request.get('session_guest4')
        session_guest5 = self.request.get('session_guest5')
        place_type = self.request.get('place_type') 
        
        #send data to datastore
        current_session = Meetup(
            name=session_name,
            event_admin=app_user.email(),
            guest1=session_guest1,
            guest2=session_guest2,
            guest3=session_guest3,
            guest4=session_guest4,
            guest5=session_guest5,
            type_of_places=place_type)
        
        current_session.put()

        #fetch user lat and long here with the email

        #calculate center lat and long

        #send that lat and long to jinja template and access that data with jquery

        template_vars = {
            'session_name': session_name,
            'place_type':place_type
            }

        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/account', AccountHandler),
    ('/event' , EventHandler),
], debug=True)
