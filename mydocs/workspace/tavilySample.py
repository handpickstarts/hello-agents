from tavily import TavilyClient
from urllib3 import response

client = TavilyClient(api_key="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")
response = client.search(query = "长沙在天气晴朗下最值得去的旅游景点推荐及理由",search_depth="basic", include_answer=True)
print(response)