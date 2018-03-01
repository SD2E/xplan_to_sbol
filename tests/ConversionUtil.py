

class SBOLNamespace():
	HTTPS_HS = 'https://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/'
	HTTP_HS = 'http://hub.sd2e.org/user/sd2e/transcriptic_rule_30_q0_1_09242017/'
	PURL_NS = 'http://purl.org/dc/terms/'
	SD2_NS = 'http://sd2e.org#'

	DESCRIPTION_NS = PURL_NS + 'description'
	TITLE_NS = PURL_NS + 'title'
	OPERTYPE_NS = SD2_NS + 'operatorType'

# Returns a new string from the SBOL URI without the given homespace attached to the original string
# Otherwise, None is returned if the given homespace wasn't found in the given URI
def removeHomespace(hs, uri):
	if uri.startswith(hs):
		return uri.replace(hs, '') 
	return None

# Returns a new string from the given uri without the given version number appended to the end of the original string
# Otherwise, None is returned if the version number wasn't found in the given URI
def removeVersion(version, uri):
	rmv = "/" + version
	if uri.endswith(rmv):
		return uri[:-len(rmv)] 
	return None

