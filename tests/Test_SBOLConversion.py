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


   def test_SBOLFiles_diff(self):
      rule30_json = 'example/xplan/rule30-Q0-v2.json'
      rule30_sbol = 'example/sbol/rule30-Q0-v2.xml'
      om_path = 'example/om/om-2.0.rdf'

      expected_sbol = Document()
      expected_sbol.read(rule30_sbol)


      with open(file) as jsonFile:
         jsonData = json.load(jsonFile)
         converted_sbol =  xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)
         outputFile = 'example/sbol/convertedResult.xml'
         converted_sbol.write(outputFile)
         actual_sbol = Document()
         actual_sbol.read(outputFile)

         # Warning! This test case will fail if the SBOL Document produced from xplan2sbol conversion 
         # has not been written to an .xml file
         sbolDiff_res = SearchQuery.compare(expected_sbol, actual_sbol)
         self.assertTrue(sbolDiff_res == 1)


if __name__ == '__main__':
	unittest.main()

