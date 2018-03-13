import json
import pySBOLx
import unittest

from tests import TestUtility
from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

class TestConversion2(unittest.TestCase):

   
    
    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        rule30_json = 'example/xplan/r30_t2.json'
		
        om_path = 'example/om/om-2.0.rdf'
        with open(rule30_json) as jsonFile:
            jsonData = json.load(jsonFile)
            cls.xplanData = XplanDataParser(jsonData)
            cls.sbolDoc = xbol.convert_xplan_to_sbol(jsonData, SBOLNamespace.HTTPS_HS, om_path, True)

    def test_Transformations2Activities_size(self):
        self.assertEqual(len(self.sbolDoc.activities), 3)

    def test_activity_ids(self):
        expected_ids = TestUtility.get_ID_List(self.xplanData)
        for i in expected_ids:
            activity = self.sbolDoc.find(i)
            self.assertIsNotNone(activity)