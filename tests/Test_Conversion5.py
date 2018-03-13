import json
import pySBOLx
import unittest

from tests import TestUtility
from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

class TestConversion5(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        rule30_json = 'example/xplan/r30_t5.json'
		
        om_path = 'example/om/om-2.0.rdf'
        with open(rule30_json) as jsonFile:
            jsonData = json.load(jsonFile)
            cls.xplanData = XplanDataParser(jsonData)
            cls.sbolDoc = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)

            cls.attachment_tl = []
            cls.experiment_tl = []
            cls.experimentalData_tl = []
            cls.implementation_tl = []
            cls.measure_tl = []
            cls.unit_tl = []

            for topLevel in cls.sbolDoc:
                if topLevel.type == SBOLNamespace.ATTACHMENT_NS:
                    cls.attachment_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENT_NS:
                    cls.experiment_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENTAL_DATA_NS:
                    cls.experimentalData_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.IMPLEMENTATION_NS:
                    cls.implementation_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.MEASURE_NS:
                    cls.measure_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.UNIT_NS:
                    cls.unit_tl.append(topLevel)
                else:
                    # Note this will warn for Activity objects
                    print("Warning! Unexpected SBOL object was found: " + topLevel.type)

    def test_Measurements2ExperimentalData_size(self):
        self.assertEqual(len(self.experimentalData_tl), 73)

    def test_Measurements2Activity_size(self):
        self.assertEqual(len(self.sbolDoc.activities), 73)

    def test_activity_ids(self):
        expected_ids = TestUtility.get_ID_List(self.xplanData)
        for i in expected_ids:
            activity = self.sbolDoc.find(i)
            self.assertIsNotNone(activity)



