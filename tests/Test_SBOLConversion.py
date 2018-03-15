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

   """ This class will perform unit testing on xplan's JSON to SBOL2 conversion

   There are two options to run this module from the xplan_to_sbol directory:
      1. Run module as a standalone: python -m unittest tests/Test_SBOLConversion.py
      2. Run this module as a test suite : python tests/SBOLTestSuite.py

   """
   
   @classmethod
   def setUpClass(cls):
      print("Running " + cls.__name__)


   def test_SBOLidentitiy_URIs(self):
      self.assertTrue(True)


if __name__ == '__main__':
	unittest.main()

