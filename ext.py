class TornadoMultiDict(object):
	# pass in self.request.arguments from requestHandler in tornado
	# it is a normal dict with lists for the value
	def __init__(self, arguments):
		self.arguments = arguments

	def __iter__(self):
		return iter(self.arguments)

	def __len__(self):
		return len(self.arguments)

	def __contains__(self, key):
		return key in self.arguments

	def getlist(self, key):
		if key in self.arguments:
			return self.arguments[key]
		else:
			return None
