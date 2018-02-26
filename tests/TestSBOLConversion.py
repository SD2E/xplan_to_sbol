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

	def test_ModDef(self):
		self.assertEqual(True, True)

	# def test_SBOL_files(self):
	# 	sbolFile = 'example/sbol/yeastGates-Q0-v2.xml'
	# 	sbolDoc = Document()
	# 	sbolDoc.read(sbolFile)
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
