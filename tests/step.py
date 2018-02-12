class step:
	''' Each step in the xplan data are stored as a step object '''

	def __init__(self, stepData):
		self.__stepKeys = stepData.keys()
		self.__step_id = stepData.get('id', None)
		self.__step_name = stepData.get('name', None)
		
		self.__step_operator = []
		

	def add_operator(self, operator):
		self.__step_operator.append(operator)

	# Returns the id assigned to this step object
	def get_id(self):
		return self.__step_id

	# Return a list of keys that are properties of this step object
	def get_keys(self):
		return self.__stepKeys

	# Returns the name assigned to this step if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_name(self):
		return self.__step_name

	# Returns a list of operator objects associated to this step
	def get_operatorList(self):
		return self.__step_operator