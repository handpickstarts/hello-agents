import os
import sys
import types
import unittest
from unittest.mock import patch, MagicMock
import importlib.util

# 提供假的 tavily 模块以避免未安装依赖导致导入失败
fake_tavily = types.ModuleType("tavily")

class _FakeTavilyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
    def search(self, **kwargs):
        return {"answer": "FAKE"}

fake_tavily.TavilyClient = _FakeTavilyClient
sys.modules["tavily"] = fake_tavily

# 加载目标模块（避免执行 __main__ 之外的代码）
MODULE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "code",
    "chapter1",
    "FirstAgentTest.py",
)

spec = importlib.util.spec_from_file_location("FirstAgentTest", MODULE_PATH)
FirstAgentTest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FirstAgentTest)


class TestFirstAgentFunctions(unittest.TestCase):
    def test_get_weather_success(self):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {
            "current_condition": [
                {"weatherDesc": [{"value": "晴"}], "temp_C": "25"}
            ]
        }
        with patch("requests.get", return_value=mock_resp):
            result = FirstAgentTest.get_weather("北京")
        self.assertIn("北京当前天气：晴，气温25摄氏度", result)

    def test_get_attraction_answer_present(self):
        class DummyTavily:
            def __init__(self, api_key: str):
                self.api_key = api_key
            def search(self, **kwargs):
                return {"answer": "推荐：外滩"}

        with patch.object(FirstAgentTest, "TavilyClient", DummyTavily):
            with patch.dict(os.environ, {"TAVILY_API_KEY": "test_key"}, clear=False):
                result = FirstAgentTest.get_attraction("上海", "晴")
        self.assertEqual("推荐：外滩", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
