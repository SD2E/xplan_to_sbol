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

class TestR30_6(unittest.TestCase):

    """ 
    This class will perform unit testing on xplan2sbol conversion for rule of 30 example.
    
    1. Run module as a standalone: python -m unittest tests/Test_Conversion6.py
    
    """

    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        rule30_json = 'example/xplan/r30_t6.json'
		
        om_path = 'example/om/om-2.0.rdf'
        with open(rule30_json) as jsonFile:
            jsonData = json.load(jsonFile)
            cls.xplanData = XplanDataParser(jsonData)
            cls.sbolDoc = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)

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
        self.assertEqual(len(self.attachments_tl), 8)
        self.assertEqual(len(self.attachments_tl), len(self.sbol_idDict.get_attachment_idList()))

    def test_Measurements2Experiment_size(self):
        self.assertEqual(len(self.experiments_tl), 1)
        self.assertEqual(len(self.experiments_tl), len(self.sbol_idDict.get_experiments_idList()))

    def test_ComponentDefinition_size(self):
        self.assertEqual(len(self.sbolDoc.componentDefinitions), 0)
        self.assertEqual(len(self.sbolDoc.componentDefinitions), len(self.sbol_idDict.get_componentDefinition_idList()))

    def test_ModuleDefinition_size(self):
        self.assertEqual(len(self.sbolDoc.moduleDefinitions), 0)
        self.assertEqual(len(self.sbolDoc.moduleDefinitions), len(self.sbol_idDict.get_moduleDefinition_idList()))

    def test_Measure_size(self):
        self.assertEqual(len(self.measures_tl), 0)
        self.assertEqual(len(self.measures_tl), len(self.sbol_idDict.get_measures_idList()))

    def test_Unit_size(self):
        self.assertEqual(len(self.units_tl), 0)
        self.assertEqual(len(self.units_tl), len(self.sbol_idDict.get_units_idList()))

    def test_Activity_ids(self):
        expected_ids = self.sbol_idDict.get_activity_idList()
        actual_ids = set()
        for a in self.sbolDoc.activities:
            actual_ids.add(a.identity)
        self.assertEqual(expected_ids, actual_ids)

    def test_Attachment_ids(self):
        expected_ids = self.sbol_idDict.get_attachment_idList()
        actual_ids = set()
        for a in self.attachments_tl:
            actual_ids.add(a.identity)
        self.assertEqual(expected_ids, actual_ids)

    def test_Implementation_ids(self):
        expected_ids = self.sbol_idDict.get_implementations_idList()
        actual_ids = set()
        for a in self.implementations_tl:
            actual_ids.add(a.identity)
        self.assertEqual(expected_ids, actual_ids)

    def test_Experiment_ids(self):
        expected_ids = self.sbol_idDict.get_experiments_idList()
        actual_ids = set()
        for a in self.experiments_tl:
            actual_ids.add(a.identity)
        self.assertEqual(expected_ids, actual_ids)

    def test_ExperimentalData_ids(self):
        expected_ids = self.sbol_idDict.get_experimentalData_idList()
        actual_ids = set()
        for a in self.experimentalData_tl:
            actual_ids.add(a.identity)
        self.assertEqual(expected_ids, actual_ids)


