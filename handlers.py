import datetime
import tornado.web
import tornado.websocket
from forms import RegistrationForm
from models import User, Room
from ext import TornadoMultiDict

# this is a global variable
room = Room()

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		"""
			This method will return None if user_id is not presented
			Or the id cannot be found inside the room.
		"""
		id = self.get_secure_cookie('user_id')
		if id in room.users:
			return room.users[id]


class RoomHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('room.html')


class RegisterHandler(BaseHandler):
	def get(self):
		# feed new registration form to users
		form = RegistrationForm()
		self.render('register.html', form=form)

	def post(self):
		form = RegistrationForm(TornadoMultiDict(self.request.arguments))
		if form.validate():
			# generate new user in the memory from POST data
			user = User(form.name.data, form.birthday.data, form.gender.data, form.country.data)
			# save the user in the memory, supposingly save it in the db of sorts
			room.users.join(user)
			# set the client cookie, since no expires_days, it is a session cookie
			self.set_secure_cookie('user_id', user.id, expires_days=None)
			# redirect to room page
			self.redirect('/')
		else:
			# return the populated form back to users with corresponding errors
			self.render('register.html', form=form)


class ChatHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		pass

	def on_message(self, message):
		self.write_message(u"You said: " + message)

	def on_close(self):
		print "WebSocket closed"