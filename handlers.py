import datetime
import json
import tornado.web
import tornado.websocket
from forms import RegistrationForm
from models import User, Room, Message
from ext import TornadoMultiDict

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		"""
			This method will return None if user_id is not presented
			Or the id cannot be found inside the room.
		"""
		id = self.get_secure_cookie('user_id')
		if id in ChatHandler.room.users:
			return ChatHandler.room.users[id]


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
			ChatHandler.room.users.join(user)
			# set the client cookie, since no expires_days, it is a session cookie
			self.set_secure_cookie('user_id', user.id, expires_days=None)
			# redirect to room page
			self.redirect('/')
		else:
			# return the populated form back to users with corresponding errors
			self.render('register.html', form=form)


class ChatHandler(tornado.websocket.WebSocketHandler):
	# class variable
	room = Room()

	def __init__(self, *args, **kwargs):
		super(ChatHandler, self).__init__(*args, **kwargs)
		self._user = None

	def open(self):
		id = self.get_secure_cookie('user_id')
		self._user = ChatHandler.room.users[id]
		# passing web socket ref to user
		self._user.ws = self

	def on_message(self, message):
		# receive front end messages
		msg = json.loads(message)
		ChatHandler.room.messages.enque(Message(self._user.id, msg['content'], msg['timestamp']));

	def on_close(self):
		# once on leave, kick user out of the room
		if self._user:
			# for debug purpose, keep it first
			pass
			# room.users.leave(self._user)
