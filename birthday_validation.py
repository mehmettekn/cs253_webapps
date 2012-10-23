import cgi
from main import *
   
months = ['Janurary', 'February', 'March', 'April', 'May',
          'June', 'July', 'August', 'September', 'October',
          'November', 'December']
######
# Validation Functions:

def valid_month(month):
     if month:
         cap_month = month.capitalize()
         if cap_month in months:
             return cap_month

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year
######
# url Handlers:

class BirthdayHandler(BaseHandler):
    def get(self):
        self.render('birthday.html')
    
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)
        error_message = 'This is not a valid date'
        if not (month and day and year):
            self.render('birthday.html', error = error_message,
						month = user_month, day = user_day,
						year = user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
        def get(self):
            self.response.out.write('Thanks thats cool')       

app = webapp2.WSGIApplication([('/birthday', BirthdayHandler),
                               ('/thanks', ThanksHandler)], debug=True)
