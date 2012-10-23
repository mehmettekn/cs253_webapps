from main import *
            
class ROT13Handler(BaseHandler):
	def get(self):
		self.render('rot13-form.html')

	def post(self):
		rot13 = ''
		text = self.request.get('text')
		if text:
			rot13 = text.encode('rot13')

		self.render('rot13-form.html', text = rot13)

app = webapp2.WSGIApplication([('/rot13', ROT13Handler)], debug=True)
