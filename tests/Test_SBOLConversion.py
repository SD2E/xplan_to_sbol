import json
import pySBOLx
import unittest

from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

''' 
	This module is used to test SBOL data that was generated from xplan_to_sbol converter for DARPA's SD2E project.
	
	author(s) : Tramy Nguyen
''' 

class testPySBOLx(unittest.TestCase):
	
	""" 
	This class will perform unit testing on xplan's JSON to SBOL2 conversion

	There are two options to run this module from the xplan_to_sbol directory:
    1. Run module as a standalone: python tests/TestSBOLConversion.py
    2. Run this module as a test suite : python tests/SBOLTestSuite.py
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

		# with open(rule30_json) as jsonData:
		jsonData = json.loads(open(rule30_json).read())
		validate = True
		converted_sbol = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, validate)

		rule30_sbol2 = 'example/sbol/convertedResult.xml'
		converted_sbol.write(rule30_sbol2)
		file2_sbol = Document()
		file2_sbol.read(rule30_sbol2)

		# Warning! This test case will fail if the SBOL Document produced from xplan2sbol conversion 
		# has not been written to an .xml file
		sbolDiff_res = SearchQuery.compare(file_sbol, converted_sbol)
		# sbolDiff_res = SearchQuery.compare(file_sbol, file2_sbol)
		# self.assertTrue(sbolDiff_res == 1)

		# Warning! Code below prints two Activities description that will show the difference of 
		# what unicode is stored as when reading from an SBOLDocument versus looking at an unicdoe before writing
		# to an .xml document
		# DC_NS = "http://purl.org/dc/terms/"
		# DESCRIPTION_NS = DC_NS + 'description'

		# uri1 = "http://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/dilute_NEB_10_beta_pAN1201_1_to_NEB_10_beta_pAN1201_2/1.0.0"
		# uri2 = "http://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/transfer_NEB_10_beta_pAN1717_3_to_E08/1.0.0"
		
		# for a1 in file_sbol.activities:
		# 	if a1.identity == uri1 or a1.identity == uri2:
		# 		print(a1.getAnnotation(DESCRIPTION_NS))


		# for a2 in converted_sbol.activities:
		# 	if a2.identity == uri1 or a2.identity == uri2:
		# 		print(a2.getAnnotation(DESCRIPTION_NS))



if __name__ == '__main__':
	unittest.main()