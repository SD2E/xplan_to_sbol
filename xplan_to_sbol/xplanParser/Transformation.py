class Transformation:
	''' Each transformations object found in xplan are stored as pyton transformations objects '''

	def __init__(self, transData):
		self.__transKeys = transData.keys()

		self.__destination = transData.get('destination', None)
		self.__od = transData.get('od600', None)  # TODO: Check for future inconsistency
		self.__volume = transData.get('volume', None)

		self.__source = []

	def add_source(self, source):
		self.__source.append(source)

	# Returns the destination assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_destination(self):
		return self.__destination

	# Return a list of keys that are properties of this tranformation object
	def get_keys(self):
		return self.__transKeys

	# Returns the od assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_od(self):
		return self.__od

	# Returns a list of source objects associated to this transformation object
	def get_sourceList(self):
		return self.__source

	# Returns the volume assigned to this transformation if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_volume(self):
		return self.__volume