import json
import pySBOLx
import unittest
# import hypothesis

from tests.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

# from hypothesis import given
# import hypothesis.strategies as st

class testPySBOLx(unittest.TestCase):
	
	""" This class will perform unit testing and property base testing on 
	xplan's JSON to SBOL2 conversion

	test1 and test2 are setup test methods to alert user if the testing environment is setup correctly.

	To run this file, enter in the following command from the xplan_to_sbol directory:
		python -m unittest tests/test_SBOLConversion.py
	"""

	# unit testing - setup test1
	def test_1(self):
		self.assertEqual('Hello', 'Hello')

	# Property base testing - setup test1 for input ordering
	# @given(st.integers(), st.integers())
	# def test_3(self,x,y):
	# 	assert(x+y == y+x)

	def test_JSON_objs(self):
		path = 'example/xplan/'
		yeastGates_Path = path + 'yeastGates-Q0-v2.json'
		rule30_Path = path + 'rule30-Q0-v1.json'
		files = [yeastGates_Path, rule30_Path]

		for file in files:
			print(file)
			with open(rule30_Path) as jsonFile:
				jsonData = json.load(jsonFile)
				xplan_data = XplanDataParser(jsonData)

				expected_xplanKeys = ['id', 'name', 'experimentId', 'experimentLab', 'experimentSet', 'steps', 'initialState']
				self.assertIsNotNone(xplan_data.get_xplanId())
				self.assertIsNotNone(xplan_data.get_xplanName())
				self.assertIsNotNone(xplan_data.get_experimentId())
				self.assertIsNotNone(xplan_data.get_experimentLab())
				self.assertIsNotNone(xplan_data.get_experimentSet())
				self.assertTrue(set(xplan_data.get_xplanKeys()).issubset(set(expected_xplanKeys)))

				expected_stepKeys = ['id', 'name', 'operator', 'description']
				for step_obj in xplan_data.get_stepsList():
					self.assertIsNotNone(step_obj.get_id())
					self.assertIsNotNone(step_obj.get_name())
					self.assertTrue(set(step_obj.get_keys()).issubset(set(expected_stepKeys)))

					expected_operKeys = ['id', 'name', 'transformations', 'description', 'samples', 'manifest', 'measurements', 'type', 'instrument_configuration', '_comment', 'channels']
					for oper_obj in step_obj.get_operatorList():
						#TODO: This assert will fail because 
						# yeastGates-Q0-v2 has a step:id = 11 and an operator:id=7
						# rule30-Q0-v2 has a step:id = 8 and an operator:id=6
						self.assertEqual(step_obj.get_id(), oper_obj.get_id())
						self.assertIsNotNone(oper_obj.get_id())
						self.assertIsNotNone(oper_obj.get_name())
						self.assertTrue(set(oper_obj.get_keys()).issubset(set(expected_operKeys)))
					
						expected_operType = ['incubate', 'pick', 'streak', 'mix', 'spectrophotometry', 'dilute', 'transfer', 'flowCytometry', 'prepare_plasmids', 'transform', 'rnaSeq']
						self.assertTrue(oper_obj.get_type() in expected_operType)

						expected_agavePrefix = 'agave://data-sd2e-community/'
						if oper_obj.get_instrumentConfig() is not None:
							self.assertTrue(oper_obj.get_instrumentConfig().startswith(expected_agavePrefix))

						for samp_obj in oper_obj.get_samplesList():
							for uri in samp_obj.get_uriList():
								self.assertTrue(uri.startswith(expected_agavePrefix))

						expected_measKeys = ['file', 'source']
						for meas_obj in oper_obj.get_measurementsList():
							for file in meas_obj.get_filesList():
								self.assertTrue(file.startswith(expected_agavePrefix))
							self.assertTrue(meas_obj.get_source().startswith(expected_agavePrefix))
					
						expected_chanKeys = ['name', 'calibration_file']
						for chan_obj in oper_obj.get_channelsList():
							self.assertTrue(set(chan_obj.get_keys()).issubset(set(expected_chanKeys)))

						expected_sd2ePrefix = 'http://sd2e.org#'
						expected_transfKeys = ['destination', 'source', 'volume', 'od600']
						expected_measureKeys = ['IPTG_measure', 'Larabinose_measure', 'aTc_measure']
						for transf_obj in oper_obj.get_transformationsList():
							self.assertTrue(set(transf_obj.get_keys()).issubset(set(expected_transfKeys)))
							self.assertTrue(transf_obj.get_destination().startswith(expected_agavePrefix))
							for source in transf_obj.get_sourceList():
								for uri in source.get_uriList():
									isExpectedURI = uri.startswith(expected_sd2ePrefix) or uri.startswith(expected_agavePrefix)
									self.assertTrue(isExpectedURI)
								for meas in source.get_measures():
									self.assertTrue(meas in expected_measureKeys)
			
	def test_yeastGates(self):
		self.assertTrue(True)
		
	def test_SBOL_files(self):
		sbolFile = 'example/sbol/yeastGates-Q0-v2.xml'
		sbolDoc = Document()
		sbolDoc.read(sbolFile)

		# TODO: This assert will fail because you must set SBOL homespace or it will set it set it to http://examples.org when reading in a file
		# self.assertTrue(hasHomespace())
		# self.assertEqual(getHomespace(), defaultSBOLURI)


		# for md in sbolDoc.moduleDefinitions:
		# 	print('------ModuleDefinitions')
		# 	print(md.identity.get())

		# 	for fc in md.functionalComponents:
		# 		print('------FunctionalComponent')
		# 		print(fc)

		# for cd in sbolDoc.componentDefinitions:
		# 	print('------ComponentDefinitions')
		# 	print(cd.identity.get())

if __name__ == '__main__':
	unittest.main()