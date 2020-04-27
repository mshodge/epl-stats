import mechanicalsoup
import time
import pandas as pd
import os
from tqdm import tqdm


browser = mechanicalsoup.StatefulBrowser()

try:
	"""Try and load a previous dataframe first"""
	df = pd.read_csv(os.path.join(os.getcwd(), 'data/premier_league_player_stats.csv'))
except FileNotFoundError:
	"""If none exist then create a blank dataframe"""
	df = pd.DataFrame(columns=['id', 'name', 'position', 'nationality', 'clubs', 'seasons', 'num_of_seasons', 'apps', 'wins',
								'losses', 'clean_sheets', 'assists', 'goals'])

def get_overview(id):
	"""Get the overview stats from the overview page"""

	browser.open(f"https://www.premierleague.com/players/{id}/player/overview")
	page = browser.get_current_page()

	try:
		name = str(page.find("div", class_="name t-colour").string)
	except AttributeError:
		return None, None, None, None, None, None

	try:
		nationality = str(page.find("span", class_="playerCountry").string)
	except AttributeError:
		nationality = None

	position = str(page.find("div", class_="info").string)

	if position == 'None':
		"""For some newer players, website format changes"""
		position = page.find_all("div", class_="info")[1].text

	clubs = []
	clubs_result = page.find_all("span", class_="long")
	for club_result in clubs_result:
		if club_result.string not in clubs:
			clubs.append(str(club_result.string))

	seasons = []
	seasons_result = page.find_all("td", class_="season")
	for season_result in seasons_result:
		if season_result.string not in seasons:
			seasons.append(str(season_result.string))

	num_of_seasons = len(seasons)
	return name, nationality, position, clubs, seasons, num_of_seasons

def get_stats(id, position):
	"""Get the detailed stats from the stats page"""

	browser.open(f"https://www.premierleague.com/players/{id}/player/stats")
	page = browser.get_current_page()

	try:
		goals = int(page.find("span", class_="allStatContainer statgoals").string)
	except AttributeError:
		return None, None, None, None, None, None

	assists = int(page.find("span", class_="allStatContainer statgoal_assist").string)
	try:
		clean_sheets = int(page.find("span", class_="allStatContainer statclean_sheet").string)
	except AttributeError:
		clean_sheets = 0

	apps = int(page.find_all("span", class_="allStatContainer statappearances")[0].string)
	wins = int(page.find_all("span", class_="allStatContainer statwins")[0].string)
	losses = int(page.find_all("span", class_="allStatContainer statlosses")[0].string)

	return clean_sheets, goals, assists, apps, wins, losses


pbar = tqdm(range(4700,17000))

for id in pbar:
	"""Run for all players"""

	if id not in df.id.to_list():
		"""Only run for players not already collected"""

		name, nationality, position, clubs, seasons, num_of_seasons = get_overview(id)
		if name is not None:
			clean_sheets, goals, assists, apps, wins, losses = get_stats(id, position)
			df_tmp = pd.DataFrame(
				[[id, name, position, nationality, clubs, seasons, num_of_seasons, apps, wins, losses, clean_sheets, assists, goals]],
				columns = ['id', 'name', 'position', 'nationality', 'clubs', 'seasons', 'num_of_seasons', 'apps', 'wins', 'losses', 'clean_sheets', 'assists', 'goals'])
			df = df.append(df_tmp)

		if id % 100 == 0:
			"""Save every 100 calls"""
			time.sleep(5)
			df.to_csv(os.path.join(os.getcwd(), 'data/premier_league_player_stats.csv'), index=False)



