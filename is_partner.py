import requests
import json
from urllib import parse
from openai import OpenAI
from config import OPENAI_API_KEY  # Import API_KEY from config

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


def playerMastery(riotId):
    userNickname, tagLine = riotId.split('#')
    encodedName = parse.quote(userNickname)
    url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encodedName}/{tagLine}"
    player_id = requests.get(url, headers=REQUEST_HEADERS).json()
    puuid = player_id['puuid']

    # Get player champion mastery info
    playerInfo = requests.get(f"https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", headers=REQUEST_HEADERS).json()

    # Extract and map championId to champion name and level
    champion_data = [{'championName': champion_id_to_name.get(str(champ['championId']), 'Unknown'), 'championLevel': champ['championLevel']} for champ in playerInfo]

    # Print the extracted champion name and level
    return champion_data[:5]

def checkCompatibility(user1, user2):
    template = """
    너는 나와 내 친구의 챔피언 숙련도를 바탕으로 듀오를 하기 적합한지 판단하는 AI야. 우리의 주 라인과 주 챔피언들에 따라 우리가 듀오를 하기 적합한지를 판단해야 해.
    보통 주포지션이나 부포지션이 탑-정글, 미드-정글, 원딜-서폿으로 매칭될 수 있으면 좋아. 한글로 대답해줘. 챔피언 이름이 지금 영어로 들어갈 텐데, 한글로 번역해서 알려줘.
    아래에 몇개의 예시를 줄게.
    ---
    Q:
    A:

    Q:
    A:
    
    Q:
    A:
    """
    user = """
    Q: 나의 챔피언 숙련도는 
    """
    user += user1
    user += """
    이고, 친구의 챔피언 숙련도는
    """
    user += user2
    user += """
    이야.
    A:
    """
    client = OpenAI(api_key=OPENAI_API_KEY)  # Use the API key
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": user}
        ]
    )
    print(user)
    return completion.choices[0].message.content


def main():
    print('본인의 Riot Id를 써주세요. 예) Hide on bush#KR1')
    riotId = input()
    print(playerMastery(riotId))
    user1 = str(playerMastery(riotId))
    print('친구의 Riot Id를 써주세요. 예) Hide on bush#KR1')
    riotId = input()
    print(playerMastery(riotId))
    user2 = str(playerMastery(riotId))
    print(checkCompatibility(user1, user2))


main()