

class SBOLNamespace():
	HTTPS_HS = 'https://hub.sd2e.org/user/sd2e/'
	HTTP_HS = 'http://hub.sd2e.org/user/sd2e/'
	TRANSCRIPTIC_NAME = 'transcriptic_rule_30_q0_1_09242017/'
	TRANSCRIPTIC_HS = HTTPS_HS + TRANSCRIPTIC_NAME
	
	AGAVE_HS = 'agave://data-sd2e-community/'
	SBOL_NS = 'http://sbols.org/v2#'
	PROV_NS = 'http://www.w3.org/ns/prov#'
	PURL_NS = 'http://purl.org/dc/terms/'
	SD2_NS = 'http://sd2e.org#'

	ACTIVITY_NS = PROV_NS + 'Activity'
	ATTACHMENT_NS = SD2_NS + 'Attachment'
	EXPERIMENT_NS = SD2_NS + 'Experiment'
	EXPERIMENTAL_DATA_NS = SD2_NS + 'ExperimentalData'
	IMPLEMENTATION_NS = SD2_NS + 'Implementation'
	MEASURE_NS = SD2_NS + 'Measure'
	UNIT_NS = SD2_NS + 'Unit'

	DISPLAYID_NS = SBOL_NS + 'displayId'
	DESCRIPTION_NS = PURL_NS + 'description'
	TITLE_NS = PURL_NS + 'title'
	OPERTYPE_NS = SD2_NS + 'operatorType'

	VERSION_1_0_0 = "1.0.0"
	VERSION_1 = "1"

# Returns a new string from the SBOL URI without the given homespace attached to the original string
# Otherwise, the original uri is returned
def removeHomespace(hs, uri):
	if uri.startswith(hs):
		return uri.replace(hs, '') 
	return uri

# Returns a new string from the given uri without the given version number appended to the end of the original string
# Otherwise, the original uri is returned
def removeVersion(version, uri):
	rmv = "/" + version
	if uri.endswith(rmv):
		return uri[:-len(rmv)] 
	return uri

def replace_uriChar(uri):
        replace_char = ['/', '-', '.']
        new_uri = uri
        for c in replace_char:
            new_uri = new_uri.replace(c, '_')
        return new_uri

