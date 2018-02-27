import json
import pySBOLx
import unittest
import os 

from XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

''' 
	This module is used to test data generated from xplan to sbol for the rule of 30 challenge problem.
	
	author(s) : Tramy Nguyen
''' 

class TestRule30(unittest.TestCase):
	
	""" 
	This class will perform unit testing on the rule of 30 example that was generated by xplan2sbol converter.

	Run this module as a test suite from the xplan_to_sbol directory: python tests/SBOLTestSuite.py
	"""
	@classmethod
	def setUpClass(cls):
		print("Running " + cls.__name__)
		rule30_json = 'example/xplan/rule30-Q0-v2.json'		
		rule30_sbol = 'example/sbol/rule30-Q0-v2.xml'
		
		cls.sbolDoc = Document()
		cls.sbolDoc.read(rule30_sbol)
		
		with open(rule30_json) as jsonFile:
				jsonData = json.load(jsonFile)
				cls.xplan_data = XplanDataParser(jsonData)

		PURL_NS = 'http://purl.org/dc/terms/'
		TITLE_NS = PURL_NS + 'title'

	def test_totalIds(self):
		expected_ids = list(range(0, 11))
		actual_ids = []
		for step_obj in self.xplan_data.get_stepsList():
			actual_ids.append(step_obj.get_id())
		self.assertEqual(expected_ids, actual_ids)

if __name__ == '__main__':
	unittest.main()