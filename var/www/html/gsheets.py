import urllib2
import csv

########################################################################
########################################################################
# Wow this is shitty but working code...

def getSheet(url):
	output = []
	lut = []
	
	data = urllib2.urlopen(url)
	sheet = csv.reader(data, delimiter=',', quotechar='"')
	
	isFirst = True
	for row in sheet:
		
		# Use first row to build index.
		if isFirst:
			for cell in row:
				lut.append(cell)
			
			isFirst = False
			continue
		
		rowDictionary = {}
		
		index = 0
		for cell in row:
			lutEntry = lut[index]
			rowDictionary[lutEntry] = cell
			index = index + 1
		
		output.append(rowDictionary)
	
	return output

########################################################################
########################################################################
# Get 'New' Scouting Data
# TODO: Make less heavy weight, perhaps add a layer of abstraction behind YADB or something...
def getScoutingData():

	# Magic Variables
	url = 'http://docs.google.com/spreadsheets/d/1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE/export?format=csv&id=1UC-p8tweVsMb38MScRZoLjKAZjGfT-jKrgHQzE_AoXE'
	
	# Create dictionary to return at end.
	teamData = {}
	
	################################################################
	# Process Raw Data
	
	# Open spreadsheet
	data = urllib2.urlopen(url)
	matchReader = csv.reader(data, delimiter=',', quotechar='"')
	
	# Iterate over the data, ignoring the first entry.
	ignoreFirst = True
	for matchData in matchReader:
		
		# Ignore the first entry, since it is just an index.
		if ignoreFirst:
			ignoreFirst = False
			continue
		
		# Pull the match number and team number out for convenience.
		matchNumber = matchData[1]
		teamNumber = matchData[2]
		
		# Create the team entry if not already present.
		if teamNumber not in teamData:
			teamData[teamNumber] = {
				'auto': {
					'spyBox': {
						'count': 0,
					},
					'autoLine': {
						'count': 0,
						'reachesOuterWorks': 0,
						'defensesBreached': {
							'None': 0,
							'Portcullis': 0,
							'Cheval de Frise': 0,
							'Moat': 0,
							'Ramparts': 0,
							'Drawbridge': 0,
							'Sally Port': 0,
							'Rock Wall': 0,
							'Rough Terrain': 0,
							'Low Bar': 0,
						},
					},
					'goals': {
						"scoredLow": 0,
						"missedLow": 0,
						"scoredHigh": 0,
						"missedHigh": 0,
					},
					'goalsByMatch': {},
				},
				'teleop': {
					'defensesBreached': {
						'None': 0,
						'Portcullis': 0,
						'Cheval de Frise': 0,
						'Moat': 0,
						'Ramparts': 0,
						'Drawbridge': 0,
						'Sally Port': 0,
						'Rock Wall': 0,
						'Rough Terrain': 0,
						'Low Bar': 0,
					},
					'goals': {
						"scoredLow": 0,
						"attemptedLow": 0,
						"scoredHigh": 0,
						"attemptedHigh": 0,
					},
					'goalsByMatch': {},
				},
				'endgame': {},
				'matches': {},
				'comments': {},
			}
		
		# Check for duplicates.
		# TODO: Handle gracefully.
		multipleEntries = matchNumber in teamData[teamNumber]['matches']

		# Get initial data from row.
		teamData[teamNumber]['matches'][matchNumber] = {
			'meta': {
				'timestamp': matchData[0],
				'multiEntry': multipleEntries,
				'version': 2,
			},
			'auto': {
				'startingPosition': matchData[3],
				'reachesOuterWorks': matchData[4],
				'defenseBreachedRaw': matchData[5],
				'defensesBreached': {},
				'goalAttemptRaw': matchData[6],
				'goalAttempt': {},
			},
			'teleop': {
				'targetsLowGoal': False,
				'scoresLowGoal': False,
				'lowGoalAttempt': matchData[7],
				'lowGoalScored': matchData[8],
				'targetsHighGoal': False,
				'scoresHighGoal': False,
				'highGoalAttempt': matchData[9],
				'highGoalScored': matchData[10],
				'defensesBreachedRaw': matchData[11],
				'defensesBreached': {},
			},
			'endgameRaw': matchData[12],
			'endgame': 0,
			'comments': {
				matchData[13],
			}
		}
		
		################################################################
		# Validate data.
		
		# TODO: Check for some common-sense dependencies.
		
		################################################################
		# Deal with multiple comments.
		
		# TODO: Do
		
		################################################################
		# Parse match autonomous mode data.
		
		# teamData.teamNumber.matches.matchNumber.auto.defenseBreachedRaw -> teamData.teamNumber.matches.matchNumber.auto.defensesBreached
		# teamData.teamNumber.matches.matchNumber.auto.goalAttemptRaw -> teamData.teamNumber.matches.matchNumber.auto.goalAttempt
		
		################################################################
		# Parse match teleop mode data.
		
		# Match Teleop
		# teamData.teamNumber.matches.matchNumber.teleop.lowGoalAttempt -> teamData.teamNumber.matches.matchNumber.teleop.targetsLowGoal
		# teamData.teamNumber.matches.matchNumber.teleop.lowGoalScored -> teamData.teamNumber.matches.matchNumber.teleop.scoresLowGoal
		# teamData.teamNumber.matches.matchNumber.teleop.highGoalAttempt -> teamData.teamNumber.matches.matchNumber.teleop.targetsHighGoal
		# teamData.teamNumber.matches.matchNumber.teleop.highGoalScored -> teamData.teamNumber.matches.matchNumber.teleop.scoresHighGoal
		
		################################################################
		# Parse match endgame data.
		
		# Match Endgame
		# teamData.teamNumber.matches.matchNumber.endgameRaw -> teamData.teamNumber.matches.matchNumber.endgame
		
		################################################################
		# Sum to produce team data.
		
		# TODO: Check for some common-sense dependencies.
		
	return teamData
