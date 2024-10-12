# main.py
from openai import OpenAI
from config import API_KEY  # Import API_KEY from config
from skill import Garen
lane, champ = input().split()
partner = input()

template = """
너는 어떤 유저의 최근 플레이 결과를 입력으로 받아서, 
해당 유저가 나와 잘 맞는 유저인지를 만드는 AI야.
나는 주로
"""
template += lane
template += "를 가고, "
template += champ
template += "가 주 챔피언이야."

few_shot = """
이 사람의 챔피언 폭을 줄테니, 내 주 챔피언과 궁합을 자세히 설명해줘.
"""
few_shot += partner
few_shot += "A:"

print(template)
print(few_shot)
client = OpenAI(api_key=API_KEY)  # Use the API key
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": template},
        {"role": "user", "content": few_shot}
    ]
)

print(completion.choices[0].message.content)