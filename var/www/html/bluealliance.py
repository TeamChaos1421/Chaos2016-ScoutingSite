import httplib
import json

########################################################################
########################################################################
# Get match schedule from TheBlueAlliance

def getMatches(event='2016lake'):
	conn = httplib.HTTPConnection('www.thebluealliance.com')
	conn.request('GET', '/api/v2/event/'+event+'/matches', '', {'X-TBA-App-Id': 'frc1421:scouting-site:v2'})
	response = conn.getresponse()
	data = response.read()
	conn.close()
	
	return json.loads(data)

########################################################################
########################################################################
# Get list of teams in match from The Blue Alliance

def getMatch(match, event='2016lake'):
	matches = getMatches(event=event)
	return
