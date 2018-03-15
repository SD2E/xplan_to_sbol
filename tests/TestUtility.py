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

    def create_SBOL_identities_v1_0_0(self, identityName):
        return  SBOLNamespace.HTTPS_HS + "/" + identityName + "/" + SBOLNamespace.VERSION_1_0_0

    def create_SBOL_identities_v1(self, identityName):
        return  SBOLNamespace.HTTPS_HS + "/" + identityName + "/" + SBOLNamespace.VERSION_1

    def remove_HS(self, uri, useChildHS):
        if uri.startswith(SBOLNamespace.TRANSCRIPTIC_HS) and useChildHS:
            return removeHomespace(SBOLNamespace.TRANSCRIPTIC_HS, uri)
        elif uri.startswith(SBOLNamespace.HTTPS_HS):
            return removeHomespace(SBOLNamespace.HTTPS_HS, uri)
        elif uri.startswith(SBOLNamespace.AGAVE_HS):
            return removeHomespace(SBOLNamespace.AGAVE_HS, uri)
        return None

    def get_uri_name(self, uri):
        # Note: this is specifically removing a transcriptic URI and version 1. 
        uriVer = self.remove_HS(uri, True)
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
                uriName = self.get_uri_name(uri)
                activity_id = self.create_SBOL_identities_v1_0_0(oper_obj.get_type() + "_" + uriName)
                implemen_id = self.create_SBOL_identities_v1_0_0(uriName)
                self.__activity_idList.add(activity_id)
                self.__implementations_idList.add(implemen_id)

    def set_measIDList(self, oper_obj):
        for meas_obj in oper_obj.get_measurementsList():
            sourceName = self.get_uri_name(meas_obj.get_source())
            for file in meas_obj.get_filesList():
                tempFile = self.remove_HS(file, False)
                fileName = replace_uriChar(tempFile)
                attachme_id = self.create_SBOL_identities_v1(fileName)
                self.__attachement_idList.add(attachme_id)
            activity_id = self.create_SBOL_identities_v1_0_0(oper_obj.get_type() + "_" + sourceName + "_to_" + sourceName + "_" + oper_obj.get_type() + "_" + str(oper_obj.get_id()))
            implemen_id = self.create_SBOL_identities_v1(sourceName)
            expData_id = self.create_SBOL_identities_v1(sourceName + "_" + oper_obj.get_type() + "_" + str(oper_obj.get_id()))
            self.__activity_idList.add(activity_id)
            self.__implementations_idList.add(implemen_id)
            self.__experimentalData_idList.add(expData_id)

    def set_transfIDList(self, oper_obj):
        for transf_obj in oper_obj.get_transformationsList():
            dest_uri = transf_obj.get_destination()
            destName = self.get_uri_name(dest_uri)
            dest_id = self.create_SBOL_identities_v1(destName)
            self.__implementations_idList.add(dest_id)

            sourceName = ""
            for source_obj in transf_obj.get_sourceList():
                for uri in source_obj.get_uriList():
                    uriName = self.get_uri_name(uri) + "_"
                    sourceName = sourceName + uriName
                    source_id = self.create_SBOL_identities_v1(self.get_uri_name(uri))
                    self.__implementations_idList.add(source_id)

            activity_id = self.create_SBOL_identities_v1_0_0(oper_obj.get_type() + "_" + sourceName + "to_" + destName)
            self.__activity_idList.add(activity_id)

