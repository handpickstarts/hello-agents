AGENT_SYSTEM_PROMT = """
你是一个智能旅行助手。你的任务是解决用户的需求，你可以使用可用工具来一步步来解决问题。

# 可用工具
- getWeather(city: str) : 根据城市获取到城市天气
- getAdvice(city: str,weather: str) : 根据城市和天气，获取旅行的建议

# 行动格式
你的回答必须要严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动。每次回复只输出一对Thought-Action。
Thought: [这里是你的思考过程和下一步计划]
Action: [这里是你需要调用的工具，格式为 function_name(arg_name="arg_value")]

# 任务完成
当你觉得你收集到足够的信息，已经完成用户提出的需求时，你必须在`Action:`字段后面使用`finish(answer="...")`来输出最终答案。

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
    url = f"https://wttr.in/{city}?format=j1"
    try:
        print(f"-调用天气API,城市:{city}")
        response = requests.get(url)
        response.raise_for_status
        data = response.json()
                
        # 提取当前天气状况
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
        
        # 格式化成自然语言返回
        return f"{city}当前天气：{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        return f"错误:查询天气时遇到网络问题 - {e}"    
    except (KeyError, IndexError) as e:
        return f"错误：解析天气数据失败，可能是城市名称无效 - {e}"
     
    
from tavily import TavilyClient
import os

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY") 
print("TAVILY_API_KEY:",TAVILY_API_KEY)

def getAdvice(city : str,weather : str) -> str:
    """
    根据城市和天气，获取旅行的建议
    """
    print(f"-调用Tavily API,城市:{city},天气:{weather}")    
    api_key = TAVILY_API_KEY # 推荐方式
    if not api_key:
        return "错误：未配置TAVILY_API_KEY环境变量"
    query = f"{city}在{weather}天气下最适合的旅游景点推荐及理由"
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
        return f"-错误：查询旅行建议时遇到问题 - {e}"
    
    
available_tools = {
    "getWeather": getWeather,
    "getAdvice": getAdvice,
}

from openai import OpenAI

class LlmClient:
    def __init__(self,api_key : str,model : str,base_url : str):
        self.model = model
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        
    def generate(self,user_promt : str,system_promt: str) -> str:
        print("-正在调用大模型")
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

import re
import os

# openai
# LLM_API_KEY = os.environ.get("OPENAI_API_KEY")
# BASE_URL = None
# MODEL_ID = "gpt-4o-mini"

# ds
# LLM_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
# BASE_URL = os.environ.get("DEEPSEEK_BASE_URL")
# MODEL_ID = "deepseek-reasoner"

# ollama
LLM_API_KEY = None
BASE_URL = "http://127.0.0.1:11434/v1"
MODEL_ID = "deepseek-r1:7b"
print(f"使用模型:{MODEL_ID}\n" + f"LLM_API_KEY:{LLM_API_KEY}\n" + f"BASE_URL:{BASE_URL}")

llmClient = LlmClient(api_key=LLM_API_KEY,model=MODEL_ID,base_url=BASE_URL)

user_promt = f"你好，请帮我查询一下今天长沙的天气，然后根据天气推荐一个合适的旅游景点。"
promt_history = [f"用户请求:{user_promt}"]

print(f"用户请求:{user_promt}\n"+ "="*40)

for i in range(1,5):
    print(f"--- 循环 {i} ---\n")
    # 1.构建promt
    full_promt = "\n".join(promt_history)
    # 2、模型思考
    llm_output = llmClient.generate(user_promt=full_promt,system_promt=AGENT_SYSTEM_PROMT)
    print(f"-大模型回复:{llm_output}")
    # 输出会有多余的Thought-Action对，需要通过正则表示patter匹配截取，只取第一个
    th_ac_pattern = r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)'
    match = re.search(th_ac_pattern, llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
    else:
        print("-未匹配到有效Thought-Action对")
        break        
    print("-截取到的有效回复Thought-Action对:",llm_output)
    promt_history.append(llm_output)
    # 3.解析获取Action，并执行行动
    action_pattern = r'Action: (.*)'
    action_match = re.search(action_pattern,llm_output,flags=re.DOTALL)
    
    if not action_match:
        print("-模型未输出有效Action")
        break
    action_str = action_match.group(1).strip()
    print("-解析到的Action: " + action_str)

    # 4 结束解析
    if action_str.startswith("finish"):
        finish_pattern = r'finish:\(answer:"(.*)"\)'
        finish_match = re.search(finish_pattern,llm_output,flags=re.DOTALL)
        # finish = finish_match.group(1).strip()
        print("-任务完成，最终答案为:",finish)
        break
    
    # 5 执行行动 Action:(tool_name(arg_key="arg_value"))
    tool_name = re.search(r'(\w+)\(',action_str,re.DOTALL).group(1)
    args_str = re.search(r'\((.*?)\)',action_str,re.DOTALL).group(1)
    kwargs = dict(re.findall(r'(\w+):"([^"]*)"',args_str))
    print(f"-解析工具方法名:{tool_name},参数键值对:{kwargs}")

    if tool_name in available_tools:
        print(f"-有可用工具{tool_name}")
        tool_fun = available_tools[tool_name]
        print(f"-执行工具方法 {tool_fun}")
        observation = available_tools[tool_name](**kwargs)
    else:
        observation =  f"-错误：未定义的工具 '{tool_name}'"
    observation_str = f"Observation: {observation}"
    print(f'{observation_str}\n' + "="*40)
    promt_history.append(observation_str)



