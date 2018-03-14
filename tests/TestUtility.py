from xplan_to_sbol.ConversionUtil import *
from xplan_to_sbol.xplanParser.XplanDataParser import XplanDataParser

class SBOLTestUtil():

    def __init__(self, xplanData):
        self.__activity_idList = set()
        self.__attachement_idList = set()
        self.__componentDefinition_idList = set()
        self.__experiments_idList = set()
        self.__experimentalData_idList = set()
        self.__implementations_idList = set()
        self.__measures_idList = set()
        self.__moduleDefinition_idList = set()
        self.__units_idList = set()

        self.set_SBOL_ids(xplanData)

    def get_activity_idList(self):
        return self.__activity_idList

    def get_attachment_idList(self):
        return self.__attachement_idList

    def get_componentDefinition_idList(self):
        return self.__componentDefinition_idList

    def get_experiments_idList(self):
        return self.__experiments_idList

    def get_experimentalData_idList(self):
        return self.__experimentalData_idList

    def get_implementations_idList(self):
        return self.__implementations_idList

    def get_measures_idList(self):
        return self.__measures_idList

    def get_moduleDefinition_idList(self):
        return self.__moduleDefinition_idList

    def get_units_idList(self):
        return self.__units_idList

    def create_SBOL_identities(self, identityName):
        return  SBOLNamespace.HTTPS_HS + "/" + identityName + "/" + SBOLNamespace.VERSION_1

    def get_uri_name(self, uri):
        # Note: this is specifically removing a transcriptic URI and version 1. 
        # This will need to be modified for diverse sample files in the future
        uriVer = removeHomespace(SBOLNamespace.TRANSCRIPTIC_HS, uri)
        return removeVersion("1", uriVer)

    def set_SBOL_ids(self, xplanData):
        # TODO: This is restricted to removing TRANSCRIPTIC URI from xplan's id. Need to expand this at one point. 
        xplan_id = xplanData.get_xplanId()
        https_pos = xplan_id.find(SBOLNamespace.HTTPS_HS) + len(SBOLNamespace.HTTPS_HS)
        trans_pos = xplan_id.find(SBOLNamespace.TRANSCRIPTIC_NAME)
        new_str = xplan_id[:https_pos] + "/" + xplan_id[trans_pos:]
        self.__experiments_idList.add(new_str)

        for step_obj in xplanData.get_stepsList():
            for oper_obj in step_obj.get_operatorList():
                if oper_obj.has_transformations():
                    self.set_transfIDList(oper_obj)
                if oper_obj.has_samples():
                    self.set_sampsIDList(oper_obj)
                if oper_obj.has_measures():
                    self.set_measIDList(oper_obj)
    
    def set_sampsIDList(self, oper_obj):
        for samp_obj in oper_obj.get_samplesList():
            for uri in samp_obj.get_uriList():
                uriName = get_uri_name(uri)
                activity_id = self.create_SBOL_identities(oper_obj.get_type() + "_" + uriName)
                self.__activity_idList.add(activity_id)

    def set_measIDList(self, oper_obj):
        for meas_obj in oper_obj.get_measurementsList():
            self.get_uri_name(measVer)
            activity_id = self.create_SBOL_identities(oper_obj.get_type() + "_" + measName + "_to_" + measName + "_" + oper_obj.get_type() + "_" + str(oper_obj.get_id()))
            self.__activity_idList.add(activity_id)

    def set_transfIDList(self, oper_obj):
        for transf_obj in oper_obj.get_transformationsList():
            dest_uri = transf_obj.get_destination()
            destName = self.get_uri_name(dest_uri)
            dest_id = SBOLNamespace.HTTPS_HS + "/" + destName + "/1"
            self.__implementations_idList.add(dest_id)

            sourceName = ""
            for source_obj in transf_obj.get_sourceList():
                for uri in source_obj.get_uriList():
                    uriName = self.get_uri_name(uri) + "_"
                    sourceName = sourceName + uriName
                    source_id = SBOLNamespace.HTTPS_HS + "/" + self.get_uri_name(uri) + "/1"
                    self.__implementations_idList.add(source_id)

            activity_id = self.create_SBOL_identities(oper_obj.get_type() + "_" + sourceName + "to_" + destName)
            self.__activity_idList.add(activity_id)

