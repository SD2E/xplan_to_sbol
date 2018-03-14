import json
import pySBOLx
import unittest

from tests.TestUtility import SBOLTestUtil
from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

class TestConversion3(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        rule30_json = 'example/xplan/r30_t3.json'
		
        om_path = 'example/om/om-2.0.rdf'
        with open(rule30_json) as jsonFile:
            jsonData = json.load(jsonFile)
            cls.xplanData = XplanDataParser(jsonData)
            cls.sbolDoc = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)

            cls.sbol_idDict = SBOLTestUtil(cls.xplanData) 

            cls.attachments_tl = []
            cls.experiments_tl = []
            cls.experimentalDatas_tl = []
            cls.implementations_tl = []
            cls.measures_tl = []
            cls.units_tl = []
            # print(cls.sbolDoc.writeString())
            for topLevel in cls.sbolDoc:
                if topLevel.type == SBOLNamespace.ATTACHMENT_NS:
                    cls.attachments_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENT_NS:
                    cls.experiments_tl.append(topLevel)
                elif topLevel.type == SBOLNamespace.EXPERIMENTAL_DATA_NS:
                    cls.experimentalDatas_tl.append(topLevel)
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

    def test_Samples2Activities_size(self):
        self.assertEqual(len(self.sbolDoc.activities), 3)

    def test_activity_ids(self):
        expected_ids = self.sbol_idDict.get_activity_idList()
        for i in expected_ids:
            activity = self.sbolDoc.find(i)
            self.assertIsNotNone(activity)