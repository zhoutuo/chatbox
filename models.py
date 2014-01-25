import uuid
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
	

class UserPool(object):
	"""
		A class to manage users in a room implemented using a dictionary.
	"""
	def __init__(self):
		self._pool = {}

	def __contains__(self, user_id):
		return user_id in self._pool

	def __getitem__(self, user_id):
		return self._pool[user_id]

	def join(self, user):
		# this will overwrite the user with the same ID, since we are
		# using UUID to generate unique ID, I do not think overwriting will happen
		self._pool[user.id] = user

	def leave(self, user):
		# set default value to None in case the user is not inside the pool
		self._pool.pop(user.id, None)

	
class MessageQueue(object):
	"""
		A class to manage messages from users in a queue ordered by the time received by the server.
		Due to concurrency issue, the order is not gauranteed.
		This implementation uses Queue class from Python standard lib which supports multi-threading already
	"""
	def __init__(self):
		# infinite size
		self._queue = Queue()

	def enque(self, message):
		self._queue.put(message)

	def deque(self):
		# block is turned on by default, which means this will wait until the queue is not empty
		return self._queue.get()


class Room(object):
	"""
		The class for a chat room, keeping track of the current in-room users in a normal dict using users' IDs as keys.
		It provides methods when a user joins or leaves the room and provides users search by IDs.
		It also saves latest messages sent by users, push them back to users.
	"""
	def __init__(self):
		self.users = UserPool()
		self.messages = MessageQueue()

	def push(self):
		"""
			Push new messages back to current users in this room if any message available.
		"""
		new_msg = self.messages.deque()

