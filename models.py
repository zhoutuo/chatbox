import uuid
import json
import weakref
from Queue import Queue

class User(object):
	"""
		A class holds the information of each uesr in a chat room.
	"""
	def __init__(self, name, bday, gender='U', country='ZZ'):
		# generate random UUID HEX string for users
		self._id = uuid.uuid4().hex
		self._name = name
		# this should be a datetime.date instance
		self._bday = bday
		self._gender = gender
		self._country = country
		# web socket connection
		self._ws = None

	@property
	def id(self):
	    return self._id
	
	@property
	def name(self):
	    return self._name

	@property
	def gender(self):
	    return self._gender

	@property
	def birthday(self):
	    return self._bday

	@property
	def country(self):
	    return self._country

	@property
	def ws(self):
		# since this is a weak ref, call()
	    return self._ws()
	@ws.setter
	def ws(self, value):
		# we use weakref in case of cyclic referencing
	    self._ws = weakref.ref(value)
	


class Message(object):
	"""
		A class stands for the message sent by users in a chat room
	"""
	def __init__(self, user_id, content, timestamp):
		self._user_id = user_id
		self._content = content
		self._timestamp = timestamp

	@property
	def user_id(self):
	    return self._user_id
	
	@property
	def content(self):
	    return self._content
	
	@property
	def timestamp(self):
	    return self._timestamp

	def to_JSON(self):
		"""
			Return a JSON string for this class
		"""
		return json.dumps(self, default=lambda o:dict(user_id=self.user_id, content=self.content, timestamp=self.timestamp))
	

class UserPool(dict):
	"""
		A class to manage users in a room implemented using a dictionary.
	"""
	def join(self, user):
		# this will overwrite the user with the same ID, since we are
		# using UUID to generate unique ID, I do not think overwriting will happen
		self[user.id] = user

	def leave(self, user):
		# set default value to None in case the user is not inside the pool
		self.pop(user.id, None)

	
class MessageQueue(object):
	"""
		A class to manage messages from users in a queue ordered by the time received by the server.
		Due to concurrency issue, the order is not gauranteed.
		callback here is the function to call when a message is added into queue
	"""
	def __init__(self, callback):
		# infinite size
		self._queue = Queue()
		self._cb = callback

	def enque(self, message):
		self._queue.put(message)
		self._cb(self.deque())

	def deque(self):
		return self._queue.get()


class Room(object):
	"""
		The class for a chat room, keeping track of the current in-room users in a normal dict using users' IDs as keys.
		It provides methods when a user joins or leaves the room and provides users search by IDs.
		It also saves latest messages sent by users, push them back to users.
	"""
	def __init__(self):
		self.users = UserPool()
		self.messages = MessageQueue(self.push)

	def push(self, new_msg):
		"""
			This is a callback function for message queue variable
			Push new messages back to current users in this room if any message available.
		"""
		for user_id in self.users:
			self.users[user_id].ws.write_message(new_msg.to_JSON())

