import json
import pySBOLx
import unittest

from XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

''' 
	This module is used to test SBOL data that was generated from xplan_to_sbol converter for DARPA's SD2E project.
	
	author(s) : Tramy Nguyen
''' 

class testPySBOLx(unittest.TestCase):
	
	""" 
	This class will perform unit testing on xplan's JSON to SBOL2 conversion

	There are 2 options to run this test module:
		1. Run this module independently from other test modules: python -m unittest TestSBOLConversion.py
		2. Run this module as a test suite: python tests/SBOLTestSuite.py
	"""

	@classmethod
	def setUpClass(cls):
		print("Running " + cls.__name__)

	def test_SBOLFiles_diff(self):
		self.assertEqual(True, True)
		rule30_json = 'example/xplan/rule30-Q0-v2.json'		
		rule30_sbol = 'example/sbol/rule30-Q0-v2.xml'
		om_path = 'example/om/om-2.0.rdf'

		file_sbol = Document()
		file_sbol.read(rule30_sbol)

		jsonData = json.loads(open(rule30_json).read())
		exp_space = 'http://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017'
		validate = True
		converted_sbol = xbol.convert_xplan_to_sbol(jsonData, exp_space, om_path, validate)

		sbolDiff_res = SearchQuery.compare(file_sbol, converted_sbol)
		self.assertTrue(sbolDiff_res == 1)


if __name__ == '__main__':
	unittest.main()
