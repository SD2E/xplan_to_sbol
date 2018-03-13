from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

def get_ID_List(xplan_data):
    expected_idList = []
    for step_obj in xplan_data.get_stepsList():
        for oper_obj in step_obj.get_operatorList():
            if oper_obj.has_transformations():
                expected_idList = expected_idList + get_transfIDList(oper_obj)
            if oper_obj.has_samples():
                expected_idList = expected_idList + get_sampsIDList(oper_obj)
            if oper_obj.has_measures():
                expected_idList = expected_idList + get_measIDList(oper_obj)
    return expected_idList

def get_sampsIDList(oper_obj):
    expected_idList = []
    for samp_obj in oper_obj.get_samplesList():
        for uri in samp_obj.get_uriList():
            uriVer = removeHomespace(SBOLNamespace.HTTPS_HS, uri)
            uriName = removeVersion("1", uriVer)
            expected_id = SBOLNamespace.HTTPS_HS + "/" + oper_obj.get_type() + "_" + uriName + "/" + SBOLNamespace.VERSION_1
            expected_idList.append(expected_id)
    return expected_idList

def get_measIDList(oper_obj):
    expected_idList = []
    for meas_obj in oper_obj.get_measurementsList():
        measVer = removeHomespace(SBOLNamespace.HTTPS_HS, meas_obj.get_source())
        measName = removeVersion("1", measVer)
        expected_id = SBOLNamespace.HTTPS_HS + "/" + oper_obj.get_type() + "_" + measName + "_to_" + measName + "_" + oper_obj.get_type() + "_" + str(oper_obj.get_id()) + "/" + SBOLNamespace.VERSION_1 
        expected_idList.append(expected_id)
    return expected_idList

def get_transfIDList(oper_obj):
    expected_idList = []
    for transf_obj in oper_obj.get_transformationsList():
        destVer = removeHomespace(SBOLNamespace.HTTPS_HS, transf_obj.get_destination())
        destName = removeVersion("1", destVer)
        sourceName = ""
        for source_obj in transf_obj.get_sourceList():
            for uri in source_obj.get_uriList():
                uriVer = removeHomespace(SBOLNamespace.HTTPS_HS, uri)
                uriName = removeVersion("1", uriVer) + "_" 
                sourceName = sourceName + uriName 
        expected_id = SBOLNamespace.HTTPS_HS + "/" + oper_obj.get_type() + "_" + sourceName + "to_" + destName + "/" + SBOLNamespace.VERSION_1 
        expected_idList.append(expected_id)
    return expected_idList