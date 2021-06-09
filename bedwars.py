import requests
import json
from pprint import pprint
import config #Contains my API Key and Bot Token

API_KEY = config.api_key

modes = ['', 'eight_one_', 'eight_two_', 'four_three_', 'four_four_']

def getBedwarsInfo(call):
    r = requests.get(call)
    data = r.json()

    if data['success'] == True and str(data['player']) == 'null': # Username not in Hypixel Database
        return "ERROR - Player not found." 
        
    elif data['success'] == False and ('Malformed UUID' in data['cause']): # Non-existant Player
        return "Invalid UUID."

    if 'stats' in data['player'] and 'Bedwars' in data['player']['stats']: # Player and Bedwars stats found
        return data['player']

    else: # Player has Hypixel data, just not Bedwars
        return "ERROR - No Bedwars data found for that player"

def getData(name):
    r = requests.get(f"https://minecraft-api.com/api/uuid/{name}")
    uuid = r.text
    name_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
    data = getBedwarsInfo(name_link)
    return data

def getStats(data, data_type):
    stats_string = ""
    for stat in data_type:
        if stat not in str(data): # if they don't have a stat, skips it
            continue
        stats_string += stat + ": " + str(data[stat]) + "\n"
    return stats_string

def getHotBar(data):
    if 'favorite_slots' in data:
        return str(data['favorite_slots'])
    return f"{name} doesn't have a custom hotbar"

def getShopLayout(data):
    if 'favourites_2' in data:
        return str(data['favourites_2'])
    return f"{name} doesn't have a custom shop"

def getKD(data, mode):
    final_kills = modes[mode] + 'final_kills_bedwars'
    final_deaths = modes[mode] + 'final_deaths_bedwars'
    if final_kills in data and final_deaths in data:
        return round(float(data[final_kills]) / int(data[final_deaths]), 2)
    else:
        return 0

def getBedRatio(data, mode):
    broken = modes[mode] + 'beds_broken_bedwars'
    lost = modes[mode] + 'beds_lost_bedwars'
    if broken in data and lost in data:
        return round(float(data[broken]) / int(data[lost]), 2)
    else:
        return 0

def getStatMode(data, stat, mode):
    if (modes[mode] + stat) in data:
        return data[modes[mode] + stat]
    else:
        return 0

def getWinRatio(data, mode):
    wins = modes[mode] + 'wins_bedwars'
    games_played = modes[mode] + 'games_played_bedwars'
    if games_played == 0 or games_played not in data or wins not in data:
        return 0
    else:
        return str(round((float (data[wins]) / float(data[games_played]) * 100), 2))