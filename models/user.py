import uuid
import weakref

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