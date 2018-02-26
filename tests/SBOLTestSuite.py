import unittest

import TestSBOLConversion
import TestXplanDataParser
import TestRule30

''' 
	This module is a test suite used to execute all test modules that had been converted into the SBOL data model
	
	To run this file, enter in the following command from the xplan_to_sbol directory:
		python tests/SBOLTestSuite.py

	author(s) : Tramy Nguyen
''' 

# Returns a test suite that has all test modules categorized as xplan2sbol 
def Xplan2SBOLTestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(TestSBOLConversion)
	s2 = unittest.TestLoader().loadTestsFromModule(TestXplanDataParser)
	s3 = unittest.TestLoader().loadTestsFromModule(TestRule30)
	xplan2sbol_testSuite = unittest.TestSuite((s1, s2, s3))
	return xplan2sbol_testSuite


if __name__ == '__main__':
	x2s_suite = Xplan2SBOLTestSuite()

	testRunner = unittest.TextTestRunner()
	testRunner.run(x2s_suite)