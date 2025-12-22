AGENT_SYSTEM_PROMT = """
你是一个智能旅行助手。你的任务是解决用户的需求，你可以使用可用工具来一步步来解决问题。

# 可用工具
- getWeather(city) : 根据城市获取到城市天气
- getAdvice(city,weather) : 根据城市和天气，获取旅行的建议

# 行动格式
你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动。每一次回复只输出一对Thought-Action。
Thought: [这里是i的思考过程]
ACTION: [这里是你需要调用的工具，格式为 function_name(arg_name="arg_value")]


# 任务完成
当你觉得你收集到足够的信息，已经完成用户提出的需求时，你必须在`ACTION:`字段后面使用`finish(answer="")`来输出最终答案。

请开始吧!

"""

import requests
import json



def getWeather(city: str) -> str:
    """
    根据城市获取到城市天气,借助wttr.in API查询天气
    """
    # API断点，
    url = f"http://wttr.in/{city}/?format=j1"
    try:
     
        response = requests.get(url)
        response.raise_for_status
        
        return ""
    except requests.exceptions.RequestException as e:
        return f"错误:查询天气时遇到网络问题 - {e}"    
    except (KeyError, IndexError) as e:
        return f"错误：解析天气数据失败，可能是城市名称无效 - {e}"
    
    
from tavily import TavilyClient
def getAdvice(city : str,weather : str) -> str:
    """
    根据城市和天气，获取旅行的建议
    """
    tavily_client = TavilyClient(api_key="tvly-33333333333333333333333333333333")
    response = tavily_client.search(query=f"在{city}，{weather}的情况下，我该如何旅行？")
    return ""
    
    
    available_tools = {
    "getWeather": getWeather,
    "getAdvice": getAdvice,
}