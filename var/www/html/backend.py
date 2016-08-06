import bluealliance
import gsheets
import dbdriver

def getRawMatchData(mode='sheet_v2'):
	
	# v1 Match Data, from Bayou
	if mode == 'sheet_v1':
		return gsheets.getSheet('http://docs.google.com/spreadsheets/d/1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo/export?format=csv&id=1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo')
		
	# v2 Match Data, from Lonestar
	if mode == 'sheet_v2':
		return gsheets.getSheet('http://docs.google.com/spreadsheets/d/1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE/export?format=csv&id=1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE')
	
	# v2 Test Data
	if mode == 'sheet_v2_debug':
		return gsheets.getSheet('http://docs.google.com/spreadsheets/d/1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE/export?format=csv&id=1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE&gid=788111861')
	
	# Something else
	return {'unsupported mode'}

def getTeamsData(mode='sheet_v2'):
	matches = getRawMatchData(mode)
	teamData = {}
	
	if mode == 'sheet_v2':
		for match in matches:
			if match['Team Number'] not in teamData:
				teamData[match['Team Number']] = []
			
			teamData[match['Team Number']].append(match)
	
		return teamData
	
	return {'unsupported mode'}

def getRawTeamData(team,mode='sheet_v2'):
	matches = getRawMatchData(mode)
	teamData = []
	
	if mode == 'sheet_v2':
		for match in matches:
			if match['Team Number'] == str(team):
				teamData.append(match)
	
		return teamData
	
	return ['unsupported mode']

def getTeamMatchData(team,mode='sheet_v2'):
	rawTeamData = getRawTeamData(team,mode=mode)
	teamMatchData = {}
	
	for match in rawTeamData:
		matchNumber = match['Match Number']
		if matchNumber not in teamMatchData:
			meta = {
				'timestamp': match['Timestamp'],
				'multiEntry': False,
				'version': 2,
			}
			
			############################################################
			
			auto = {
				'startingPosition': match['Starting Position'],
				'reachedOuterWorks': match['Reaches Outer Works'],
				'defenseBreached': match['Breaches Defense'],
				'goalAttempted': 'None',
				'scored': False
			}
			
			if match['Goal'] == 'Scored Low Goal':
				auto['goalAttempted'] = 'Low Goal'
				auto['scored'] = True
			elif match['Goal'] == 'Missed Low Goal':
				auto['goalAttempted'] = 'Low Goal'
			elif match['Goal'] == 'Scored High Goal':
				auto['goalAttempted'] = 'High Goal'
				auto['scored'] = True
			elif match['Goal'] == 'Missed High Goal':
				auto['goalAttempted'] = 'High Goal'
				
			
			############################################################
			
			teleop = {
				'targetsLowGoal': False,
				'scoresLowGoal': False,
				'lowGoalAttempt': int(match['Low Goals Attempted'] or '0'),
				'lowGoalScored': int(match['Low Goals Scored'] or '0'),
				
				'targetsHighGoal': False,
				'scoresHighGoal': False,
				'highGoalAttempt': int(match['High Goals Attempted'] or '0'),
				'highGoalScored': int(match['High Goals Scored'] or '0'),
				
				'defensesBreached': {},
			}
			
			teleop['scoresLowGoal'] = (teleop['lowGoalScored'] > 0)
			teleop['targetsLowGoal'] = (teleop['lowGoalScored'] > 0) or (teleop['lowGoalAttempt'] > 0)
			
			teleop['scoresHighGoal'] = (teleop['highGoalScored'] > 0)
			teleop['targetsHighGoal'] = (teleop['highGoalScored'] > 0) or (teleop['highGoalAttempt'] > 0)
			
			for defense in match['Defenses Breached'].split(', '):
				if defense != '':
					teleop['defensesBreached'][defense] = True
				
			
			############################################################
			
			endgame = match['Endgame']
			
			############################################################
			
			comments = match['Comment']
			
			############################################################
			
			teamMatchData[match['Match Number']] = {
				'meta': meta,
				'auto': auto,
				'teleop': teleop,
				'endgame': endgame,
				'comments': comments,
			}
		else:
			teamMatchData[match['Match Number']]['meta']['multiEntry'] = True

	return teamMatchData

def getTeamData(team,mode='sheet_v2'):
	matches = getTeamMatchData(team,mode=mode)
	
	auto = {
	}
	
	####################################################################
	
	teleop = {
		'highShooter': False,
		'lowShooter': False,
		'defensesBreached': {},
	}
	
	for match in matches:		
		if matches[match]['teleop']['highGoalAttempt']:
			teleop['highShooter'] = True
			
		if matches[match]['teleop']['lowGoalAttempt']:
			teleop['lowShooter'] = True
		
		for defense in matches[match]['teleop']['defensesBreached'].keys():
			teleop['defensesBreached'][defense] = True
	
	####################################################################
	
	endgame = {
	}
	
	for match in matches:
		if matches[match]['endgame'] != '':
			endgame[matches[match]['endgame']] = True
	
	####################################################################
	
	comments = {}
	
	for match in matches:		
		comments[match] = matches[match]['comments']
	
	####################################################################
	
	parsed = {
		'auto': auto,
		'teleop': teleop,
		'endgame': endgame,
		'matches': matches,
		'comments': comments,
	}
	
	return parsed

def getMatchSchedule(mode='couchdb',event='2016txho'):
	if mode == 'tba':
		return bluealliance.getMatches(event=event)
	
	if mode == 'couchdb':
		return dbdriver.getMatches()
	
	return {'unsupported mode'}

def getMatchTeams(match,mode='couchdb',event='2016txho'):
	if mode == 'tba' or mode == 'couchdb':
		matchSchedule = getMatchSchedule(mode,event=event)
		return matchSchedule[match]
	
	return {'unsupported mode'}

def getScoutingSettings(mode='couchdb'):
	if mode == 'couchdb':
		return dbdriver.getScoutingSettings()
	
	return {'unsupported mode'}
