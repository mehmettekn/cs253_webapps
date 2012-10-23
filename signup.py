from main import *
from password import *
import re

USER_name = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_name(name):
    return name and USER_name.match(name)

USER_password = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and USER_password.match(password)

def valid_verify(password1, password2):
    return password1==password2

USER_email = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or USER_email.match(email)

class SignupHandler(BaseHandler):
    def get(self):
        self.render('signup.html')
    
    def post(self):
        error_flag = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.pass2 = self.request.get('verify')
        self.email = self.request.get('email')
        params = {'username': self.username, 'email': self.email}
        
        if not valid_name(self.username):
            params['error_username'] = 'Thats not a valid username.'
            error_flag = True
        
        if not valid_password(self.password):
            params['error_pass'] = "That's not a valid password."
            error_flag = True

        if not valid_verify(self.password, self.pass2):
            params['error_pass2'] = "Your passwords didn't match!"
            error_flag = True
        
        if not valid_email(self.email):
            params['error_email'] = "That's not a valid e-mail!"
            have_error = True

        if error_flag:
            self.render('signup.html', **params)
        else:
            self.done()
    
    def done(self, *a, **kw):
        raise NotImplementedError

class Register(SignupHandler):
	def done(self):
		u = User.by_name(self.username)
		if u:
			msg = "That user already exists!"
			self.render('signup.html', error_username = msg)
		else:
			u = User.register(self.username, self.password, self.email)
			u.put()
			self.login(u)
			self.redirect('/welcome')

class WelcomeHandler(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.username)
        else:
            self.redirect('/login')
   
class Login(BaseHandler):
    def get(self):
        self.render('login.html')
	
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = "Invalid username and password!"
            self.render('login.html', error = msg)
		

class Logout(BaseHandler):
	def get(self):
		self.logout()
		self.redirect('/login')

app = webapp2.WSGIApplication([('/signup', Register),
                               ('/welcome', WelcomeHandler),
                               ('/login', Login),
							   ('/logout', Logout)],
							   debug = True)            
