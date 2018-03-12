import unittest

from tests import Test_SBOLConversion
from tests import Test_XplanDataParser
from tests import Test_Rule30

''' 
	This module is used to create test suites for running test modules related to the SBOL Data model
	
	To run this file, enter in the following command from the xplan_to_sbol directory:
		python -m tests.SBOLTestSuite

	author(s) : Tramy Nguyen
''' 

# Returns a test suite that has all test modules categorized as xplan2sbol 
def Xplan2SBOLTestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_SBOLConversion)
	s2 = unittest.TestLoader().loadTestsFromModule(Test_XplanDataParser)
	s3 = unittest.TestLoader().loadTestsFromModule(Test_Rule30)
	xplan2sbol_testSuite = unittest.TestSuite((s1, s2, s3))
	return xplan2sbol_testSuite


if __name__ == '__main__':
	x2s_suite = Xplan2SBOLTestSuite()

	testRunner = unittest.TextTestRunner()
	testRunner.run(x2s_suite)