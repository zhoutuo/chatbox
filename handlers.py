import datetime
import tornado.web
import forms
import ext

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")


class RoomHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		pass


class RegisterHandler(BaseHandler):
	def get(self):
		form = forms.RegistrationForm()
		self.render('register.html', form=form)

	def post(self):
		form = forms.RegistrationForm(ext.TornadoMultiDict(self.request.arguments))
		if form.validate():
			self.write("Conguratulations")
		else:
			self.render('register.html', form=form)

