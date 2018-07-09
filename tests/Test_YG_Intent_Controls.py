
import json
import pySBOLx
import unittest
import sys
import argparse
from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

import xplan_to_sbol.__main__ as xbol
from sbol import *

""" 
    This module is used to test data uploaded through xplan to sbol for the YG challenge problem.
    author(s) : Mark Weston
"""
class TestYeastGates(unittest.TestCase):

    """ 
    This uploads a dummy YG plan's intent, WT, and control information
    """
    def test_intent_control_upload(self):
        yg_json = 'example/xplan/biofab_yg_UWBF_NOR_intent_control_test.json'        
        
        with open(yg_json) as json_file:
            json_data = json.load(json_file)

            # change this manually with the SBH password; getting unittest to accept custom 
            # arguments is a pain
            #FIXME: parameterize this
            password = None
            if password is not None:
                uploaded = xbol.post_upload_intent(json_data, 'https://hub.sd2e.org', 'sd2_service@sd2e.org', password)
                self.assertTrue(uploaded)

                self.assertTrue(xbol.read_intent(json_data))
            else:
                print("No password provided, skipping upload")
            control_results = xbol.post_upload_controls(json_data)
            # We should have written two triple sets
            self.assertTrue(len(control_results['results']['bindings']) == 2)
            
if __name__ == '__main__':
    unittest.main()
