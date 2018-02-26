class xplanoperator:
	''' Each operator in the xplan data are stored as a python operator object '''

	def __init__(self, operatorData):
		self.__operatorKeys = operatorData.keys()
		
		self.__id = operatorData.get('id', None)
		self.__name = operatorData.get('name', None)
		self.__comment = operatorData.get('_comment', None)
		self.__description = operatorData.get('description', None)
		self.__instConfig = operatorData.get('instrument_configuration', None)
		self.__manifest = operatorData.get('manifest', None)
		self.__type = operatorData.get('type', None)

		self.__channels = []
		self.__measurements = []
		self.__samples = []
		self.__transformations = []
		
	def add_channel(self, channel):
		self.__channels.append(channel)

	def add_measurement(self, meas):
		self.__measurements.append(meas)

	def add_sample(self, sample):
		self.__samples.append(sample)

	def add_transformation(self, transf):
		self.__transformations.append(transf)

	# Returns a list of channel objects associated to this operator
	def get_channelsList(self):
		return self.__channels

	# Returns the comment assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_comment(self):
		return self.__comment

	# Returns the description assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_description(self):
		return self.__description

	# Returns the id assigned to this operator object
	def get_id(self):
		return self.__id

	# Returns the instrument configuration assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_instrumentConfig(self):
		return self.__instConfig

	# Return a list of keys that are properties of this operation object
	def get_keys(self):
		return self.__operatorKeys

	# Returns the manifest assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_manifest(self):
		return self.__manifest

	# Returns a list of measurement objects associated to this operator
	def get_measurementsList(self):
		return self.__measurements

	# Returns the name assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_name(self):
		return self.__name

	# Returns a list of sample objects associated to this operator
	def get_samplesList(self):
		return self.__samples

	# Returns a list of transformation objects associated to this operator
	def get_transformationsList(self):
		return self.__transformations

	# Returns the type assigned to this operator if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_type(self):
		return self.__type