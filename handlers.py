import tornado.web

class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('template/register.html')