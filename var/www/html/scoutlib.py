from mod_python import apache
import backend

########################################################################
########################################################################
# Scouting Sheet

def getScoutingAssignment(match=None):
	settings = backend.getScoutingSettings(mode='couchdb')
	
	if match == None:
		match = settings['currentMatchNumber']
	
	return {
		'matches': [int(match)-1, match, int(match)+1],
		'teams': backend.getMatchTeams(match, mode='couchdb'),
		'scouts': settings['scoutingPool'],
	}

########################################################################
########################################################################
# Team Index

def getTeamList():
	matches = backend.getRawMatchData(mode='sheet_v2')
	teams = {}
	teamList = []
	
	for match in matches:
		teamNumber = match['Team Number']
		teams[teamNumber] = True
	
	for team in teams:
		teamList.append(team)
	
	return teamList

########################################################################
########################################################################
# Team Viewer

def getTeamData(team):
	teamData = backend.getTeamData(team,mode='sheet_v2')
	return teamData

########################################################################
########################################################################
# Database-ish Stuff

def updateRawScoutingSettings(scouts=None, match=None):
	dbURL = 'http://chaos.mlaga97.space:5984/'
	credentials = ('chaos','circuit')
	
	import couchdb
	
	# Open DB
	couch = couchdb.Server(dbURL)
	couch.resource.credentials = credentials
	db = couch['space/mlaga97/chaos/scouting/2016/settings']
	settings = db.get('scoutingSheetConfig')
	
	# Update
	
	if scouts != None:
		settings['scoutingPool'] = scouts
	
	if match != None:
		settings['currentMatchNumber'] = match
	
	# Submit
	return db.save(settings)

def markStale():
	dbURL = 'http://chaos.mlaga97.space:5984/'
	credentials = ('chaos','circuit')
	
	import couchdb
	
	# Open DB
	couch = couchdb.Server(dbURL)
	couch.resource.credentials = credentials
	db = couch['space/mlaga97/chaos/scouting/2016/settings']
	status = db.get('status')
	
	# Update
	status['stale'] = True
	
	# Submit
	return db.save(status)
