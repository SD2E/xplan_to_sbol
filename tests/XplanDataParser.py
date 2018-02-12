import json 

from tests.step import step
from tests.operator import operator
from tests.channel import channel
from tests.sample import sample
from tests.source import source
from tests.measurement import measurement
from tests.transformation import transformation

''' This module is used to parse xplan's data that was generated for DARPA's TA1-SD2E project.
	
	author(s) : Tramy Nguyen
''' 

class XplanDataParser():
	''' This class is a data parser for xplan's json file. 
		An instance of this class will provide a user the ability to get objects and its properties 
		found in xplan's json file.
	'''
	
	def __init__(self, xplanData):
		self.__stepsList = []

		self.__xplanKeys = xplanData.keys()
		self.__xplan_id = xplanData.get('id', None)
		self.__xplan_name = xplanData.get('name', None)
		self.__experiment_id = xplanData.get('experimentId', None)
		self.__experiment_lab = xplanData.get('experimentLab', None)
		self.__experiment_set = xplanData.get('experimentSet', None)
		
		# if 'initialState' in xplanData:
		# 	self.initStateParser(xplanData['initialState'])
		if 'steps' in xplanData:
			self.stepsParser(xplanData['steps'])

	

	def stepsParser(self, data):
		currIndex = 0
		while currIndex < len(data):
			stepData = data[currIndex]
			step_id = stepData['id']
			step_obj = step(stepData)
			self.__stepsList.append(step_obj)
			if 'operator' in stepData:
				self.operatParser(stepData['operator'], step_id, step_obj)
			currIndex = currIndex + 1

	def operatParser(self, data, step_id, step_obj):
		currIndex = 0
		# Note: There will only be one operator per step
		oper_obj = operator(data)
		if 'transformations' in data:
			self.transParser(data['transformations'], step_id, oper_obj)
		if 'measurements' in data:
			self.measParser(data['measurements'], step_id, oper_obj)
		if 'samples' in data:
			self.sampsParser(data['samples'], step_id, oper_obj)
		if 'channels' in data:
			self.channelsParser(data['channels'], step_id, oper_obj)
		step_obj.add_operator(oper_obj)
		

	def channelsParser(self, data, step_id, oper_obj):
		currIndex = 0
		while currIndex < len(data):
			chanData = data[currIndex]
			chan_obj = channel(chanData)
			oper_obj.add_channel(chan_obj)
			currIndex = currIndex+1

	def measParser(self, data, meas_id, oper_obj):
		currIndex = 0
		while currIndex < len(data):
			measData = data[currIndex]
			meas_obj = measurement(measData)
			if 'file' in measData:
				if isinstance(measData['file'], str):
					meas_obj.add_file(measData['file'])
				else:
					for file in measData['file']:
						meas_obj.add_file(file)
			oper_obj.add_measurement(meas_obj)
			currIndex = currIndex + 1

	def sampsParser(self, data, step_id, oper_obj):
		currIndex = 0
		while currIndex < len(data):
			sampsData = data[currIndex]
			samp_obj = sample()
			samp_obj.add_uri(sampsData)
			oper_obj.add_sample(samp_obj)
			currIndex = currIndex + 1

	def sourceParser(self, data, source_id, transf_obj):
		if isinstance(data, str):
			source_obj = source()
			source_obj.add_uri(data)
			transf_obj.add_source(source_obj)
		else:
			currIndex = 0
			while currIndex < len(data):
				s_id = str(source_id) + '_' + str(currIndex)
				sourceData = data[currIndex]
				source_obj = source()
				if isinstance(sourceData, dict):
					source_obj.add_measure(sourceData)
				else:
					source_obj.add_uri(sourceData)
				transf_obj.add_source(source_obj)
				currIndex = currIndex + 1

	def transParser(self, data, trans_id, oper_obj):
		currIndex = 0
		while currIndex < len(data):
			t_id = str(trans_id) + '_' + str(currIndex)
			transfData = data[currIndex]
			transf_obj = transformation(transfData)
			if 'source' in transfData:
				self.sourceParser(transfData['source'], t_id, transf_obj)
			oper_obj.add_transformation(transf_obj)
			currIndex = currIndex + 1

	# Return a list of steps object
	def get_stepsList(self):
		return self.__stepsList

	# Returns the id assigned to this xplan 
	def get_xplanId(self):
		return self.__xplan_id

	# Returns the experiment name assigned to this xplan
	def get_xplanName(self):
		return self.__xplan_name

	# Return a list of keys that are properties of this xplan
	def get_xplanKeys(self):
		return self.__xplanKeys

	# Returns the experiment id assigned to this xplan
	def get_experimentId(self):
		return self.__experiment_id

	# Returns the experiment lab assigned to this xplan
	def get_experimentLab(self):
		return self.__experiment_lab

	# Returns the experiment set assigned to this xplan
	def get_experimentSet(self):
		return self.__experiment_set






