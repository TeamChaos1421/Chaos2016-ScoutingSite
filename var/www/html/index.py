from mod_python import apache
import scoutlib

########################################################################
########################################################################
# More-or-less static index page for navigation.

def index(req):
	req.content_type = 'text/html'
	return '<center><h1>Index</h1><a href="scouting">Scouting Sheet</a><br/><a href="teams">Team Index</a><br/><a href="admin">Admin Panel</a></center>'

########################################################################
########################################################################
# Scouting sheet with chart to show assignments.

def scouting(req, match=None):
	html = '<html> <body> <div style="background-color: rgb(103, 58, 183);"> <center> <br/><br/> <div style="width: 600px; display: block; background-color: rgb(255, 255, 255);"> <br/><br/> <b> <font size="72">Match #{matches[1]}</font> <br/> <a href="scouting?match={matches[0]}">Match {matches[0]}</a> <a href="index">Back</a> <a href="scouting?match={matches[2]}">Match {matches[2]}</a> </b> <br/><br/><br/><br/> <table border="1"> <tr> <td> <b> <font size="72">Red 1</font> </b> </td> <td> <b> <font size="72">{teams[0]}</font> </b> </td> <td> <b> <font size="72">{scouts[0]}</font> </b> </td> </tr> <tr> <td> <b> <font size="72">Red 2</font> </b> </td> <td> <b> <font size="72">{teams[1]}</font> </b> </td> <td> <b> <font size="72">{scouts[1]}</font> </b> </td> </tr> <tr> <td> <b> <font size="72">Red 3</font> </b> </td> <td> <b> <font size="72">{teams[2]}</font> </b> </td> <td> <b> <font size="72">{scouts[2]}</font> </b> </td> </tr> </table> <br/><br/> <table border="1"> <tr> <td> <b> <font size="72">Blue 1</font> </b> </td> <td> <b> <font size="72">{teams[3]}</font> </b> </td> <td> <b> <font size="72">{scouts[3]}</font> </b> </td> </tr> <tr> <td> <b> <font size="72">Blue 2</font> </b> </td> <td> <b> <font size="72">{teams[4]}</font> </b> </td> <td> <b> <font size="72">{scouts[4]}</font> </b> </td> </tr> <tr> <td> <b> <font size="72">Blue 3</font> </b> </td> <td> <b> <font size="72">{teams[5]}</font> </b> </td> <td> <b> <font size="72">{scouts[5]}</font> </b> </td> </tr> </table> <br/><br/> </div> <embed src="https://docs.google.com/forms/d/{formID}/viewform?embedded=true" width="100%" height="3500" frameborder="0" marginheight="0" marginwidth="0"/> </center> </div> </body> </html>'
	
	# Get Scouting Assignment
	scoutingAssignment = scoutlib.getScoutingAssignment(match=match)
	
	# Send to Client
	req.content_type = 'text/html'
	return html.format(
		matches = scoutingAssignment['matches'],
		teams = scoutingAssignment['teams'],
		scouts = scoutingAssignment['scouts'],
		formID = "1e0JMqGwNi5XCjxPYWvC48d5MQejlpR3jsWLfssx7g7c"
	)

########################################################################
########################################################################
# Display a list of teams that have data available.

def teams(req):
	teams = scoutlib.getTeamList()
	
	outer = '<a href="index">Back</a><center><h1>Team Index</h1><p>{inner}</p></center>'
	innerTemplate = '<a href="team?team={team}">{team}</a> '
	inner = ''
	
	for team in teams:
		inner = inner + innerTemplate.format(team=team)
	
	req.content_type = 'text/html'
	return outer.format(inner=inner)

########################################################################
########################################################################
# Display summary of team using scouting data.
# TODO: Work-in-progress

import json

def team(req, team=None):
	if team == None:
		return teams(req)
	
	teamData = scoutlib.getTeamData(team)
	
	####################################################################
	
	comments = ''
	
	comment_info = {int(k) : v for k, v in teamData['comments'].items()}
	
	for match in sorted(comment_info):
		comments = comments + 'Match ' + str(match) + ': ' + teamData['comments'][str(match)] + '<br/>\n'
	
	####################################################################
	
	robot = ''
	
	####################################################################
	
	teleop = ''
	
	if teamData['teleop']['lowShooter']:
		teleop = teleop + 'Can shoot low goal.<br/>'
		
	if teamData['teleop']['highShooter']:
		teleop = teleop + 'Can shoot high goal.<br/>'
	
	if 'Successfully Scales' in teamData['endgame']:
		teleop = teleop + 'Successfully scales.<br/>'
	elif 'Attempts to Scale' in teamData['endgame']:
		teleop = teleop + 'Attempts to scale.<br/>'
	elif 'Challenges Tower' in teamData['endgame']:
		teleop = teleop + 'Challenges Tower.<br/>'
	
	teleop = teleop + '<h3>Defenses</h3>'
	for defense in teamData['teleop']['defensesBreached']:
		teleop = teleop + defense + '<br/>\n'
	
	####################################################################
	
	auto = ''
	
	####################################################################
	
	req.content_type = 'text/html'
	return '''
	<html>
		<a href="/teams">Back</a><br>
		<center><br/>
			<h1>Team {team}</h1>
			<a href="/teamJSON?team={team}">Raw scouting data (JSON)</a>
			<h2>Comments</h2>
			{comments}
			<h2>Teleop</h2>
			{teleop}
			<h2>Autonomous</h2>
			{auto}
		</center>
	</html>
	'''.format(team=team,comments=comments,teleop=teleop,auto=auto)

def teamJSON(req, team=None):
	if team == None:
		return teams(req)
	
	return json.dumps(scoutlib.getTeamData(team),indent=4)

########################################################################
########################################################################
# Display administrative page to allow changing various settings.
# TODO: Add some kind of authentication.

def admin(req):
	html = '<a href="index">Back</a><br><center><form action="adminCatch" method="get">Current Match Number<br><input type="text" name="matchNumber" value={matches[1]}><br><br>Scouts:<br><input type="text" name="scout1" value="{scouts[0]}"><br><input type="text" name="scout2" value="{scouts[1]}"><br><input type="text" name="scout3" value="{scouts[2]}"><br><input type="text" name="scout4" value="{scouts[3]}"><br><input type="text" name="scout5" value="{scouts[4]}"><br><input type="text" name="scout6" value="{scouts[5]}"><br><br><input type="submit" value="Submit"></form></center>'

	# Get Scouting Assignment
	scoutingAssignment = scoutlib.getScoutingAssignment()
	
	req.content_type = 'text/html'
	return html.format(
		scouts = scoutingAssignment['scouts'],
		matches = scoutingAssignment['matches']
	)

########################################################################
########################################################################
# Catch data from administrative page, and put them into the database.

def adminCatch(req, matchNumber=None, scout1=None, scout2=None, scout3=None, scout4=None, scout5=None, scout6=None):
	scoutlib.updateRawScoutingSettings(match=matchNumber,scouts=[scout1,scout2,scout3,scout4,scout5,scout6])
	
	req.content_type = 'text/html'
	return '<META http-equiv="refresh" content="0;URL=/admin">'

########################################################################
########################################################################
# Mark the database stale so that it may be updated

def stale(req):
	scoutlib.markStale()
	return ''

