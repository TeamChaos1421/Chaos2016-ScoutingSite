from mod_python import apache
import os
import csv
import StringIO
import urllib2
import httplib
import json

people = ["Caleb", "Anthony", "Katey", "Madeline", "Noah", "Neil"]

def index(req):
	req.content_type = 'text/html'
	req.write('<center><h1>Index</h1><a href="scouting">Scouting Sheet</a><br/><a href="teams">Team Index</a></center>')

def scouting(req, match=None):
	req.content_type = 'text/html'
	
	conn = httplib.HTTPConnection("www.thebluealliance.com")
	conn.request("GET", "/api/v2/event/2016lake/matches", "", {"X-TBA-App-Id": "frc1421:sanity-check:2"})
	response = conn.getresponse()
	data = response.read()
	conn.close()
	
	if match == None:
		match = 32
	match = int(match)
	
	
	req.write('<html><body><div style="background-color: rgb(103, 58, 183);"><center>')

	req.write('<br/><br/><div style="width: 600px; display: block; background-color: rgb(255, 255, 255);">')

	req.write('<br/><br/><b><font size="72">Match #'+str(match)+'</font><br/><a href="scouting?match='+str(match-1)+'">Match '+str(match-1)+'</a>  <a href="index">Back</a>  <a href="scouting?match='+str(match+1)+'">Match '+str(match+1)+'</a></b><br/><br/><br/><br/>')

	for entry in json.loads(data):
		if int(entry["match_number"]) == int(match):
			req.write('<table border="1">')
			req.write('<tr><td><b><font size="72">Red 1</font></b></td><td><b><font size="72">'+str(entry["alliances"]["red"]["teams"][0]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[0])+'</font></b></td></tr>')
			req.write('<tr><td><b><font size="72">Red 2</font></b></td><td><b><font size="72">'+str(entry["alliances"]["red"]["teams"][1]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[1])+'</font></b></td></tr>')
			req.write('<tr><td><b><font size="72">Red 3</font></b></td><td><b><font size="72">'+str(entry["alliances"]["red"]["teams"][2]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[2])+'</font></b></td></tr>')
			req.write('</table>')

			req.write('<br/><br/>')

			req.write('<table border="1">')
			req.write('<tr><td><b><font size="72">Blue 1</font></b></td><td><b><font size="72">'+str(entry["alliances"]["blue"]["teams"][0]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[3])+'</font></b></td></tr>')
			req.write('<tr><td><b><font size="72">Blue 2</font></b></td><td><b><font size="72">'+str(entry["alliances"]["blue"]["teams"][1]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[4])+'</font></b></td></tr>')
			req.write('<tr><td><b><font size="72">Blue 3</font></b></td><td><b><font size="72">'+str(entry["alliances"]["blue"]["teams"][2]).replace("frc", "")+'</font></b></td><td><b><font size="72">'+str(people[5])+'</font></b></td></tr>')
			req.write('</table>')

	req.write('<br/><br/></div>')

	req.write('<embed src="https://docs.google.com/forms/d/1e0JMqGwNi5XCjxPYWvC48d5MQejlpR3jsWLfssx7g7c/viewform?embedded=true" width="100%" height="3500" frameborder="0" marginheight="0" marginwidth="0"/>')

	req.write('</center></div></body></html>')
	
	return

def teams(req):
	req.content_type = 'text/html'
	
	# Print All the Teams We Have Info On
	teams = {}
	
	data = urllib2.urlopen('http://docs.google.com/spreadsheets/d/1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo/export?format=csv&id=1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo')
	matchReader = csv.reader(data, delimiter=',', quotechar='"')
	
	for row in matchReader:
		team = row[2]
		teams[team] = True
	
	req.write('<a href="index">Back</a><center><h1>Team Index</h1><p>')
	for teamNumber in teams.keys():
		if teamNumber != "Team Number" and teamNumber != "":
			req.write('<a href="team?number='+str(teamNumber)+'">'+str(teamNumber)+'</a> ')
	req.write('</p></center>')

def team(req, number):
	req.content_type = 'text/html'
	req.write('<a href="teams">Back</a><center><h1>Team #'+str(number)+'</h1>')
	
	teams = {}
	teams[number] = {}
	teams[number]["auto"] = {}
	teams[number]["teleop"] = {}
	teams[number]["goals"] = {}

	req.write('<h2>Comments</h2>')
	data = urllib2.urlopen('http://docs.google.com/spreadsheets/d/1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo/export?format=csv&id=1f31whAYg1Sbt68nCURIF3zFoB6E0mBW6f0i5QQqBXNo')
	matchReader = csv.reader(data, delimiter=',', quotechar='"')
	for row in matchReader:
		date = row[0]
		matchNum = row[1]
		team = row[2]
		auto = row[3]
		teleop = row[4]
		goals = row[5]
		comment = row[6]
		
		if team == number:
			req.write('\tMatch '+str(matchNum)+': '+str(comment)+'<br/>')
			
			autoSIO = StringIO.StringIO(auto)
			autoReader = csv.reader(autoSIO, delimiter=',')
			for autoRow in autoReader:
				for autoMode in autoRow:
					teams[number]["auto"][str(autoMode.lstrip())] = True
			
			teleopSIO = StringIO.StringIO(teleop)
			teleopReader = csv.reader(teleopSIO, delimiter=',')
			for teleopRow in teleopReader:
				for teleopMode in teleopRow:
					teams[team]["teleop"][str(teleopMode.lstrip())] = True
			
			goalsSIO = StringIO.StringIO(goals)
			goalsReader = csv.reader(goalsSIO, delimiter=',')
			for goalsRow in goalsReader:
				for goalsMode in goalsRow:
					teams[team]["goals"][str(goalsMode.lstrip())] = True

	req.write('<h2>Autonomous</h2>')
	for autoMode in teams[number]["auto"].keys():
		req.write(autoMode+'<br/>')

	req.write('<h2>Teleop</h2>')
	for teleopMode in teams[number]["teleop"].keys():
		req.write(teleopMode+'<br/>')

	req.write('<h2>Goals</h2>')
	for goalMode in teams[number]["goals"].keys():
		req.write(goalMode+'<br/>')
	
	req.write('</center>')
	
	return
