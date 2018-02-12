
class channel:

	def __init__(self, chanData):
		self.__channels_keys = chanData.keys()

		self.__calibration_file = chanData.get('calibration_file', None)
		self.__name = chanData.get('name', None)

	# Returns the calibration file assigned to this measurement if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_calibrationFile(self):
		return self.__calibration_file

	# Returns the name assigned to this channel if it was set in xplan's data. 
	# Otherwise, None is returned.
	def get_name(self):
		return self.__name

	# Return a list of keys that are properties of this channel object
	def get_keys(self):
		return self.__channels_keys
