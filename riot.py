import requests
import json
from urllib import parse

# Load champion data from JSON file
with open('./champion.json', 'r', encoding='utf-8') as f:
    champion_data = json.load(f)

# Create a mapping from champion key (id) to name
champion_id_to_name = {champ['key']: champ['name'] for champ in champion_data['data'].values()}

# Example API Key and other configurations
from config import RIOT_API_KEY
api_key = RIOT_API_KEY # 새로 발급받은 api_key

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": RIOT_API_KEY
}

userNickname = "graycat"
tagLine = "0124"
encodedName = parse.quote(userNickname)
print(encodedName)
url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encodedName}/{tagLine}"

player_id = requests.get(url, headers=REQUEST_HEADERS).json()

puuid = player_id['puuid']
url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
player = requests.get(url, headers=REQUEST_HEADERS).json()
print(player)

# Get player champion mastery info
playerInfo = requests.get(f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", headers=REQUEST_HEADERS).json()

# Extract and map championId to champion name and level
champion_data = [{'championName': champion_id_to_name.get(str(champ['championId']), 'Unknown'), 'championLevel': champ['championLevel']} for champ in playerInfo]

# Print the extracted champion name and level
print(champion_data)
