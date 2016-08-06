import httplib
import json

def getMatches():
	conn = httplib.HTTPConnection('chaos.mlaga97.space:5984')
	conn.request('GET', '/space%2Fmlaga97%2Fchaos%2Fscouting%2F2016%2Fsettings' + '/LonestarQualificationMatches')
	response = conn.getresponse()
	data = response.read()
	conn.close()
	
	return json.loads(data)

# TODO: Do something with mode.
def getScoutingSettings():
	conn = httplib.HTTPConnection('chaos.mlaga97.space:5984')
	conn.request('GET', '/space%2Fmlaga97%2Fchaos%2Fscouting%2F2016%2Fsettings' + '/scoutingSheetConfig')
	response = conn.getresponse()
	data = response.read()
	conn.close()

	return json.loads(data)
