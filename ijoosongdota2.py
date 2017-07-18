import dota2api
import json
import time
from datetime import datetime
import urllib
import smtplib

#Joe's Steam ID
steamID = 17854758
steamID3 = 35709316
steamID64 = 76561197995975044

while True:
	#Current Time
	c_Time = datetime.now()
	print c_Time
	current_Time = time.mktime(c_Time.timetuple())

	#dota2api info
	#dota2 API key
	api = dota2api.Initialise("Enter Valve API Key")

	#get Joe's Dota Match History
	hist = api.get_match_history(account_id=steamID64)

	#get Joe's Most Recent Match ID
	recent_match_id = hist['matches'][0]['match_id']

	#get Match Details
	match = api.get_match_details(match_id=recent_match_id)

	#get Joe's Solo MMR from OpenDota API
	opendota_mmr_url = "https://api.opendota.com/api/players/" + str(steamID3)
	opendota_mmr_response = urllib.urlopen(opendota_mmr_url)
	opendota_mmr = json.loads(opendota_mmr_response.read())

	#get Joe's Warding from OpenDota API
	opendota_wards_url = "https://api.opendota.com/api/matches/" + str(recent_match_id)
	opendota_wards_response = urllib.urlopen(opendota_wards_url)
	opendota_wards = json.loads(opendota_wards_response.read())

	#isolate Joe's player information from his match
	i = 0
	while i < 8:
		if match['players'][i]['account_id'] == steamID3:
			break
		else:
			i+=1

	#Most recent game timestamp
	game_time = match['start_time']
	local_time = time.strftime("%m/%d %H:%M:%S", time.localtime(game_time))

	#Time since last game in hours
	time_difference = str((current_Time - game_time)/3600)

	#What team is Joe on?
	team = match['players'][i]['player_slot']
	if team < 100:
		team = 'Radiant'
	else:
		team = 'Dire'

	#What hero did Joe pick?
	hero_picked = str(match['players'][i]['hero_name'])

	#How many times did Joe die?
	death_count = str(match['players'][i]['deaths'])

	#How many wards did Joe place/use?
	wards_placed = str(opendota_wards['players'][i]['obs_placed'])
	wards_used = str(opendota_wards['players'][i]['observer_uses'])

	#Result of the match
	results = match['radiant_win']
	if results == 'True':
		results = 'Radiant'
	else:
		results = 'Dire'

	#Joe's Solo MMR
	mmr = str(opendota_mmr['solo_competitive_rank'])

	#Print Test
	print "Last Game Played: " + time_difference + " hours ago"
	print "Game started on: " + local_time
	print "Joe's team: " + team
	print "Joe's hero: " + hero_picked
	print "Joe's Deathcount: " + death_count
	print "Wards Placed: " + wards_placed
	print "Wards Used: " + wards_used
	print "Winner: " + results
	print "Joe's Solo MMR: " + mmr

	#login gmail
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login('Enter Gmail Account', 'Enter Gmail Password')

	#Notifications
	if time_difference < 0.5:
		#send email to text
		server.sendmail('Enter Gmail Account', 'Enter Recipients Number', '\n' + 'Last game played: ' + time_difference + ' hours ago' + '\n' + 'Game started on: ' + local_time + '\n' + 'Joe\'s Team: ' + team + '\n' + 'Joe\'s hero: ' + hero_picked + '\n' + 'Joe\'s Deathcount: ' + death_count + '\n' + 'Winner: ' + results + '\n' + 'Joe\'s Solo MMR: ' + mmr)
	time.sleep(1800 - time.time() % 1800)
