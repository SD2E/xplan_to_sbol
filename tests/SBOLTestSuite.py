import unittest

from tests import Test_XplanDataParser
from tests import Test_SBOLConversion
from tests import Test_Rule30
from tests import Test_yeastGates
from tests import Test_R30_1
from tests import Test_R30_2
from tests import Test_R30_3
from tests import Test_R30_4
from tests import Test_R30_5
from tests import Test_R30_6
from tests import Test_YG_1
from tests import Test_YG_2
from tests import Test_YG_3




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

def Rule30_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_Rule30)
	s2 = unittest.TestLoader().loadTestsFromModule(Test_R30_1)
	s3 = unittest.TestLoader().loadTestsFromModule(Test_R30_2)
	s4 = unittest.TestLoader().loadTestsFromModule(Test_R30_3)
	s5 = unittest.TestLoader().loadTestsFromModule(Test_R30_4)
	s6 = unittest.TestLoader().loadTestsFromModule(Test_R30_5)
	s7 = unittest.TestLoader().loadTestsFromModule(Test_R30_6)
	rule30_testSuite = unittest.TestSuite((s1, s2, s3, s4, s5, s6, s7))
	return rule30_testSuite

def YeastGates_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_yeastGates)
	s2 = unittest.TestLoader().loadTestsFromModule(Test_YG_1)
	s3 = unittest.TestLoader().loadTestsFromModule(Test_YG_2)
	s4 = unittest.TestLoader().loadTestsFromModule(Test_YG_3)
	yeastGates_testSuite = unittest.TestSuite((s1, s2, s3, s4))
	return yeastGates_testSuite

def Xplan2SBOL_TestSuite():
	s1 = unittest.TestLoader().loadTestsFromModule(Test_SBOLConversion)
	xplan2sbol_testSuite = unittest.TestSuite(s1)
	return xplan2sbol_testSuite

if __name__ == '__main__':
	xpn_suite = Xplan_TestSuite()
	x2s_suite = Xplan2SBOL_TestSuite()
	r30_suite = Rule30_TestSuite()
	ygs_suite = YeastGates_TestSuite()
        
	testRunner = unittest.TextTestRunner()
	testRunner.run(xpn_suite)
	testRunner.run(x2s_suite)
	testRunner.run(r30_suite)
	testRunner.run(ygs_suite)	
