import json
import unittest
import os

from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

''' 
    This module is used to test xplan's data for the DARPA's SD2E project.
    
    author(s) : Tramy Nguyen
''' 

class TestXplanDataParser(unittest.TestCase):
    
    """ 
    This class will perform unit testing on XPlanDataParser.
    
    There are two options to run this module from the xplan_to_sbol directory:
    1. Run module as a standalone: python -m unittest tests/Test_XplanDataParser.py
    2. Run this module as a test suite : python tests/SBOLTestSuite.py
    
    """
    
    @classmethod
    def setUpClass(cls):
        print("Running " + cls.__name__)
        directory = 'example/xplan/'
        rule30 = directory + 'rule30-Q0-v2.json'
        yeastGates = directory + 'yeastGates-Q0-v2.json'
        cls.jsonFiles = [rule30, yeastGates]
        
    def test_Xplan_Keys(self):
        for f in self.jsonFiles:
            with open(f) as xplanFile:
                jsonData = json.load(xplanFile)
                xplan_data = XplanDataParser(jsonData)
                    
                expected_xplanKeys = ['id', 'name', 'experimentId', 'experimentLab', 'experimentSet', 'steps', 'initialState']
                self.assertIsNotNone(xplan_data.get_xplanId())
                self.assertIsNotNone(xplan_data.get_xplanName())
                self.assertIsNotNone(xplan_data.get_experimentId())
                self.assertIsNotNone(xplan_data.get_experimentLab())
                self.assertIsNotNone(xplan_data.get_experimentSet())
                self.assertTrue(set(xplan_data.get_xplanKeys()).issubset(set(expected_xplanKeys)))
                    
                expected_stepKeys = ['id', 'name', 'operator', 'description']
                for step_obj in xplan_data.get_stepsList():
                    self.assertIsNotNone(step_obj.get_id())
                    self.assertIsNotNone(step_obj.get_name())
                    self.assertTrue(set(step_obj.get_keys()).issubset(set(expected_stepKeys)))
                        
                    expected_operKeys = ['id', 'name', 'transformations', 'description', 'samples', 'manifest', 'measurements', 'type', 'instrument_configuration', '_comment', 'channels']
                    for oper_obj in step_obj.get_operatorList():
                        self.assertIsNotNone(oper_obj.get_id())
                        self.assertIsNotNone(oper_obj.get_name())
                        self.assertTrue(set(oper_obj.get_keys()).issubset(set(expected_operKeys)))
                            
                        expected_operType = ['incubate', 'pick', 'streak', 'mix', 'spectrophotometry', 'dilute', 'transfer', 'flowCytometry', 'prepare_plasmids', 'transform', 'rnaSeq']
                        self.assertTrue(oper_obj.get_type() in expected_operType)
                            
                        expected_agavePrefix = 'agave://data-sd2e-community/'
                        if oper_obj.get_instrumentConfig() is not None:
                            self.assertTrue(oper_obj.get_instrumentConfig().startswith(expected_agavePrefix))
                                
                        expected_sbhPrefix = 'https://hub.sd2e.org/user/sd2e/'
                        for samp_obj in oper_obj.get_samplesList():
                            for uri in samp_obj.get_uriList():
                                isExpectedURI = uri.startswith(expected_sbhPrefix) or uri.startswith(expected_agavePrefix)
                                self.assertTrue(isExpectedURI)
                                        
                        expected_measKeys = ['file', 'source']
                        for meas_obj in oper_obj.get_measurementsList():
                            for file in meas_obj.get_filesList():
                                isExpectedURI = file.startswith(expected_sbhPrefix) or file.startswith(expected_agavePrefix)
                                self.assertTrue(isExpectedURI)
                            isExpectedURI = meas_obj.get_source().startswith(expected_sbhPrefix) or meas_obj.get_source().startswith(expected_agavePrefix)
                            self.assertTrue(isExpectedURI)
                                
                        expected_chanKeys = ['name', 'calibration_file']
                        for chan_obj in oper_obj.get_channelsList():
                            self.assertTrue(set(chan_obj.get_keys()).issubset(set(expected_chanKeys)))
                                                    
                        expected_sd2ePrefix = 'http://sd2e.org#'
                        expected_transfKeys = ['destination', 'source', 'volume', 'od600']
                        expected_measureKeys = ['IPTG_measure', 'Larabinose_measure', 'aTc_measure']
                                                
                        for transf_obj in oper_obj.get_transformationsList():
                            self.assertTrue(set(transf_obj.get_keys()).issubset(set(expected_transfKeys)))
                            isExpectedURI = transf_obj.get_destination().startswith(expected_sbhPrefix) or transf_obj.get_destination().startswith(expected_agavePrefix)
                            self.assertTrue(isExpectedURI)
                            for source in transf_obj.get_sourceList():
                                for uri in source.get_uriList():
                                    isExpectedURI = uri.startswith(expected_sbhPrefix) or uri.startswith(expected_agavePrefix)
                                    self.assertTrue(isExpectedURI)
                                for meas in source.get_measures():
                                    self.assertTrue(meas in expected_measureKeys)
                                                            
    def test_duplicateIds(self):
        for f in self.jsonFiles:
            unique_ids = []
            duplic_ids = []
            
            with open(f) as xplanFile:
                jsonData = json.load(xplanFile)
                xplan_data = XplanDataParser(jsonData)
                
                for step_obj in xplan_data.get_stepsList():
                    if step_obj.get_id() not in unique_ids:
                        unique_ids.append(step_obj.get_id())
                    else:
                        duplic_ids.append(step_obj.get_id())
                self.assertEqual(len(duplic_ids), 0)
                
    def test_StepOperator_Ids(self):
        # Check if step id and operator id matches each other
        for f in self.jsonFiles:
            with open(f) as xplanFile:
                jsonData = json.load(xplanFile)
                xplan_data = XplanDataParser(jsonData)
                
                for step_obj in xplan_data.get_stepsList():
                    for oper_obj in step_obj.get_operatorList():
                        self.assertEqual(step_obj.get_id(), oper_obj.get_id())


if __name__ == '__main__':
	unittest.main()
