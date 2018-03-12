class Measurement:
	''' Each measurements object found in xplan are stored as pyton measurements objects '''

	def __init__(self, measData):
		self.__measKeys = measData.keys()

		# Note: Optional Field(s)
		self.__files = []
		self.__source = measData.get('source', None)
		
	def add_file(self, file):
		self.__files.append(file)
		
	# Returns a list of files associated to this measurement object
	def get_filesList(self):
		return self.__files

	# Returns the source assigned to this measurement if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_source(self):
		return self.__source

	# Return a list of keys that are properties of this measurement object
	def get_keys(self):
		return self.__measKeys