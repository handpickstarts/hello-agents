finish_answer = f'finish(answer="今天长沙的天气是晴朗，气温10摄氏度。根据这个天气，推荐的旅游景点是橘子洲，它免费开放，适合家庭游玩。")'

pattern = r'finish\(answer="(.*)"\)' 

import re

def getMatch() -> str:
    match = re.search(pattern,finish_answer,re.DOTALL)
    result = match.group(1)
    print(f"result is {result}")

getMatch()