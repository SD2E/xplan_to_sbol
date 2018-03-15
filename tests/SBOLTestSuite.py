import unittest

from tests import Test_SBOLConversion
from tests import Test_Conversion1
from tests import Test_Conversion2
from tests import Test_Conversion3
from tests import Test_Conversion4
from tests import Test_Conversion5
from tests import Test_Conversion6
from tests import Test_XplanDataParser
from tests import Test_Rule30


''' 
	This module is used to create test suites for running test modules related to the SBOL Data model
	
	To run this file, enter in the following command from the xplan_to_sbol directory:
		python -m tests.SBOLTestSuite

	author(s) : Tramy Nguyen
''' 

def Xplan_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_XplanDataParser) 
	xplan_testSuite = unittest.TestSuite(s1)
	return xplan_testSuite

def ExampleProblems_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_Rule30)
	ep_testSuite = unittest.TestSuite(s1)
	return ep_testSuite

def Xplan2SBOL_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_SBOLConversion)
	s2 = unittest.TestLoader().loadTestsFromModule(Test_Conversion1)
	s3 = unittest.TestLoader().loadTestsFromModule(Test_Conversion2)
	s4 = unittest.TestLoader().loadTestsFromModule(Test_Conversion3)
	s5 = unittest.TestLoader().loadTestsFromModule(Test_Conversion4)
	s6 = unittest.TestLoader().loadTestsFromModule(Test_Conversion5)
	s7 = unittest.TestLoader().loadTestsFromModule(Test_Conversion6)
	xplan2sbol_testSuite = unittest.TestSuite((s1, s2, s3, s4, s5, s6, s7))
	return xplan2sbol_testSuite



if __name__ == '__main__':
	x2s_suite = Xplan2SBOL_TestSuite()
	ex_suite = ExampleProblems_TestSuite()
	x_suite = Xplan_TestSuite()

	testRunner = unittest.TextTestRunner()
	testRunner.run(x_suite)
	testRunner.run(ex_suite)
	testRunner.run(x2s_suite)
	
	