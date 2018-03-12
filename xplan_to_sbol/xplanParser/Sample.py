class Sample:
	''' Each samples found in the xplan data will be stored as a python samples object '''

	def __init__(self):
		self.__uriList = []

	def add_uri(self, uri):
		self.__uriList.append(uri)

	# Returns a list of URIs associated to this sample
	def get_uriList(self):
		return self.__uriList