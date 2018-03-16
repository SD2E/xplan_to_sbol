import json
import pySBOLx
import unittest

from tests.TestUtility import SBOLTestUtil
from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

''' 
    This module is used to test xplan's data for the DARPA's SD2E project.
    
    author(s) : Tramy Nguyen
''' 

class TestYG_3(unittest.TestCase):

    """ 
    This class will perform unit testing on xplan2sbol conversion for yeastGates example.
    
    1. Run module as a standalone: python -m unittest tests/Test_YG_3.py
    2. Run this module as a test suite : python -m tests.SBOLTestSuite
    
    """

    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        rule30_json = 'example/xplan/yg_t3.json'
		
        om_path = 'example/om/om-2.0.rdf'
        with open(rule30_json) as jsonFile:
            jsonData = json.load(jsonFile)
            cls.xplanData = XplanDataParser(jsonData)
            cls.sbolDoc = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)
            # print(cls.sbolDoc.writeString())
            cls.sbol_idDict = SBOLTestUtil(cls.xplanData) 

            cls.attachments_tl = []
            cls.experiments_tl = []
            cls.experimentalData_tl = []
            cls.implementations_tl = []
            cls.measures_tl = []
            cls.units_tl = []
            
            for topLevel in cls.sbolDoc:
                if topLevel.type == SBOLNamespace.ATTACHMENT_NS:
                    cls.attachments_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENT_NS:
                    cls.experiments_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENTAL_DATA_NS:
                    cls.experimentalData_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.IMPLEMENTATION_NS:
                    cls.implementations_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.MEASURE_NS:
                    cls.measures_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.UNIT_NS:
                    cls.units_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.ACTIVITY_NS:
                    continue #No need to store this when I can directly access through sbolDoc
                else:
                    print("Warning! Unexpected SBOL object was found: " + topLevel.type)

    def test_Measurements2ExperimentalData_size(self):
        self.assertEqual(len(self.experimentalData_tl), 1)
        self.assertEqual(len(self.experimentalData_tl), len(self.sbol_idDict.get_experimentalData_idList()))

    def test_Measurement2Implementation_size(self):
        self.assertEqual(len(self.implementations_tl), 1)
        self.assertEqual(len(self.implementations_tl), len(self.sbol_idDict.get_implementations_idList()))

    def test_Measurements2Activity_size(self):
        self.assertEqual(len(self.sbolDoc.activities), 1)
        self.assertEqual(len(self.sbolDoc.activities), len(self.sbol_idDict.get_activity_idList()))

    def test_Measurements2Attachment_size(self):
        self.assertEqual(len(self.attachments_tl), 1)
        self.assertEqual(len(self.attachments_tl), len(self.sbol_idDict.get_attachment_idList()))

    def test_Measurements2Experiment_size(self):
        self.assertEqual(len(self.experiments_tl), 1)
        self.assertEqual(len(self.experiments_tl), len(self.sbol_idDict.get_experiments_idList()))
