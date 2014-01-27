import json
import uuid
import weakref
import collections
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

	def profile(self):
		return {
			"name": self.name,
			"gender": self.gender,
			# birthday is a date instance
			"birthday": self.birthday.isoformat(),
			"country": self.country		
		}


class MessageType(object):
	"""
		Acts as a enum type for Message class below
	"""
	User, Chat = range(2)


class Message(object):
	"""
		A class stands for the message sent by users in a chat room
	"""
	def __init__(self, type, user_id, timestamp, content=None):
		"""
			Content:
			0. User: User profile: Name, Gender, Birthday, Country
			1. Chat: Chat content
		"""
		self._user_id = user_id
		self._timestamp = timestamp
		self._type = type
		self._content = content

	@property
	def user_id(self):
	    return self._user_id
	
	@property
	def content(self):
	    return self._content
	@content.setter
	def content(self, value):
		self._content = value
	
	@property
	def timestamp(self):
	    return self._timestamp

	@property
	def type(self):
	    return self._type

	def to_dict(self):
		"""
			Return a JSON string for this class
		"""
		return {
			"user_id": self.user_id,
			"timestamp": self.timestamp,
			"type": self.type,
			"content": self.content
		}


class MessageWrapperType(object):
	"""
		Acts as a enum type for MessageWrapper class below
		0. Join: A user joins.
		1. Leave: A user leaves.
		2. Exist: A user exists.
		3. NewChat: A new message just sent.
		4. CacheChat: Old messages.
	"""
	Join, Leave, Exist, NewChat, CacheChat = range(5)


class MessageWrapper(object):
	"""
		A class that wraps Message.
	"""
	def __init__(self, type, messages, target=None):
		"""
			type:
			is one of the type above.
			messages:
			a list of messages wrapped, which depends on type.
			Join/Leave/NewChat len=1
			Exist/CacheChat len=0~N
			target:
			means to whom this message should be sent to,
			If no specified, which is the general case, this message will send to all users
			else, it will be only sent to these users decided by IDs.
		"""
		self._type = type
		self._messages = messages
		self._target = target

	@property
	def type(self):
	    return self._type

	@property
	def messages(self):
	    return self._messages

	@property
	def target(self):
	    return self._target

	def to_dict(self):
		"""
			for json.dumps in handlers
		"""
		return {
			"type": self._type,
			"messages": [message.to_dict() for message in self._messages]
		}


	

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
		callback here is the function to call when a message is added into queue.
		What's more, it also maintains a cache of push messages for new joined users.
	"""
	def __init__(self, callback, cache_size=20):
		"""
			The default cache size is 20 messages
		"""
		# infinite size
		self._queue = Queue()
		self._cb = callback
		self._cache = collections.deque(maxlen=cache_size)

	def enque(self, message):
		self._queue.put(message)
		self._cb(self.deque())

	def deque(self):
		new_msg = self._queue.get()
		# push into cache
		# depend on the type, only cares about NewChat type
		if new_msg.type == MessageWrapperType.NewChat:
			# extract the first message from the message list
			self._cache.extend(new_msg.messages)
		return new_msg

	def cache(self):
		"""
			Returns an iterater of the cache queue, order is from the oldest to newest message
		"""
		return self._cache.__iter__()


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
		target = new_msg.target or self.users
		for user_id in target:
			self.users[user_id].ws.write_message(json.dumps(new_msg.to_dict()))