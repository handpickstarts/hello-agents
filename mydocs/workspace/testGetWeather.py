import requests

def getWeather() -> str:
    url = "https://wttr.in/北京?format=j1"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # 提取当前天气状况
    current_condition = data['current_condition'][0]
    weather_desc = current_condition['weatherDesc'][0]['value']
    temp_c = current_condition['temp_C']
    answer = f"北京当前天气：{weather_desc}，气温{temp_c}摄氏度"
    print(f"answer is {answer}")
    return answer

getWeather()