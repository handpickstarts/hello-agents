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

from random import choice
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
    api_key = os.environ.get("TAVILY_API_KEY") # 推荐方式
    if not api_key:
        return "错误：未配置TAVILY_API_KEY环境变量"
    query = f"在{city}，{weather}的情况下，我该如何旅行？"
    try:

        tavily_client = TavilyClient(api_key= api_key)
        # include_answer 会返回一个综合性回答
        response = tavily_client.search(query=query,search_depth="basic",include_answer= True)
        # 解析返回结构体
        if response.get("answer"):
            return response["answer"]
        # 如果没有综合性回答，则格式化原始结果
        format_results = []
        for result in response.get("results",[]):
            format_results.append(f"- {result['title']}: {result['content']}")

        if not format_results:
            return "没有找到相关的旅行建议"        

        return f"以下是根据{city}和{weather}的建议：\n" + "\n".join(format_results)
    except Exception as e:
        return f"错误：查询旅行建议时遇到问题 - {e}"
    
    
available_tools = {
    "getWeather": getWeather,
    "getAdvice": getAdvice,
}

from openai import OpenAI

class LlmAgent:
    def __init__(self,api_key : str,model : str,base_url : str):
        self.model = model
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        
    def generate(self,user_promt : str,system_promt: str) -> str:
        print("正在调用大模型")
        try:
            messages = [{'role':'system','content':system_promt},
            {'role':'user','content':user_promt}]
            response = self.client.chat.completions.create(messages= messages,model= self.model,stream= False)
            answer = response.choices[0].message.content
            print("大语言模型响应成功")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误：调用语言模型服务时出错"