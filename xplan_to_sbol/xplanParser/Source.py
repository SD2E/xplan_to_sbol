class Source:

	def __init__(self):
		# This will be used to track IPTG, Larabinose, aTc measurements
		self.__measures = {}
		self.__uriList = []

	def add_measure(self, meas):
		self.__measures.update(meas)

	def add_uri(self, uri):
		self.__uriList.append(uri)

	# Returns a list of measure objects associated to this transformation object
	def get_measures(self):
		return self.__measures

	# Returns a list of URIs 
	def get_uriList(self):
		return self.__uriList
