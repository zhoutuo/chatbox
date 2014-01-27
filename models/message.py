import collections
from Queue import Queue


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