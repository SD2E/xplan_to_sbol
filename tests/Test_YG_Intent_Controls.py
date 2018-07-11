
import json
import pySBOLx
import unittest
import sys
import os
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
    This uploads a dummy YG plan's plan, sample attributes, intent, WT, and control information
    """
    def test_intent_control_upload(self):
        yg_json_path = 'example/xplan/biofab_yg_UWBF_NOR_intent_control_test.json'
        yg_json_sa_path = 'example/xplan/biofab_yg_UWBF_NOR_intent_control_test_sample_attributes.json'

        url = 'https://hub.sd2e.org'
        email = 'sd2_service@sd2e.org'

        with open(yg_json_path) as plan_json_file:
            plan_data = json.load(plan_json_file)

            # change this manually with the SBH password; getting unittest to accept custom 
            # arguments is a pain
            #FIXME: parameterize this
            password = None
            if password is not None:

                # intent
                plan_base_name = os.path.basename(yg_json_path)
                plan_id = plan_data['id']
                intent = plan_data['intent']
                intent_file_name = xbol.create_intent_file_name(plan_base_name)

                uploaded = xbol.post_upload_json(plan_id, intent, intent_file_name, url, email, password)
                self.assertTrue(uploaded)
                self.assertTrue(xbol.read_attachment(plan_id, intent_file_name))

                # plan
                uploaded = xbol.post_upload_json(plan_id, plan_data, plan_base_name, url, email, password)
                self.assertTrue(uploaded)
                self.assertTrue(xbol.read_attachment(plan_id, plan_base_name))

                # sample attributes
                sample_attributes_file_name = xbol.create_sample_attributes_file_name(plan_base_name)

                with open(yg_json_sa_path) as plan_sample_attributes_file:
                    plan_sample_attributes_data = json.load(plan_sample_attributes_file)
                    uploaded = xbol.post_upload_json(plan_id, plan_sample_attributes_data, sample_attributes_file_name, url, email, password)
                    self.assertTrue(uploaded)
                    self.assertTrue(xbol.read_attachment(plan_id, sample_attributes_file_name))
            else:
                print("No password provided, skipping upload")

            control_results = xbol.post_upload_controls(plan_data)
            # We should have written two triple sets
            self.assertTrue(len(control_results['results']['bindings']) == 2)
            
if __name__ == '__main__':
    unittest.main()
