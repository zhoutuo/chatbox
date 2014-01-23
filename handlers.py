import datetime
import tornado.web
import forms
import ext

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")


class RoomHandler(BaseHandler):
	def get(self):
		if not self.get_current_user:
			self.redirect("/register")
		else:
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

