import dota2api
import pandas as pd

#ijoosong's Steam ID
steamID = 17854758
steamID3 = 35709316
steamID64 = 76561197995975044

#Valve API Key
api = dota2api.Initialise("Enter Valve API Key")

#ijoosong's Match History
match_history = api.get_match_history(account_id=steamID64)

#List of Match ID, Match Details, Hero Picks
number_of_matches = len(match_history['matches'])
match_id = []
team = []
hero_pick = []
deaths = []
results = []


for match_number in xrange(number_of_matches):
	match_id.append(match_history['matches'][match_number]['match_id'])
	
	#List of Match Details
	match_details = api.get_match_details(match_id=match_id[match_number])
	
	#Isolate ijoosong's Match Details
	player_position = 0
	while player_position < 8:
		if match_details['players'][player_position]['account_id'] == steamID3:
			break
		else:
			player_position += 1
	
	#ijoosong's Team
	if match_details['players'][player_position]['player_slot'] < 100:
		team.append('Radiant')
	else:
		team.append('Dire')
	
	#List of Hero Picks		
	hero_pick.append(match_details['players'][player_position]['hero_name'])
	
	#Number of deaths
	deaths.append(match_details['players'][player_position]['deaths'])
	
	#Results
	if match_details['radiant_win'] == 1:
		results.append('Radiant')
	else:
		results.append('Dire')
	

df = pd.DataFrame(list(zip(match_id, team, hero_pick, deaths, results)), columns=['Match ID', 'Team', 'Hero Picked', 'Deaths', 'Results'])
df.to_csv('ijoosong.csv', index=False)

print 'done'
