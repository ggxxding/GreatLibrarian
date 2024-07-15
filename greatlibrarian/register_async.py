import unittest
from unittest.mock import MagicMock
import asyncio


class Test(unittest.TestCase):
    """A class to test the LLM to be registered"""

    def __init__(self, llm, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.llm = llm

    async def test_api_response(self, mock_post) -> bool:
        result = await self.llm("你好")
        print(f"API_response result:{result}")
        if isinstance(result, str):
            return True
        else:
            return False


class Register_Async:
    """A class to register the LLM"""

    def __init__(self, conf) -> None:
        self.test_llm = conf.test_llm
        self.LLM_eval_llm = conf.LLM_eval_llm

    async def checkllm(self) -> bool:
        testobj1, testobj2 = self.test_llm, self.LLM_eval_llm
        test1, test2 = Test(testobj1), Test(testobj2)
        mock_post = MagicMock()
        api_response1 = await test1.test_api_response(mock_post)
        api_response2 = await test2.test_api_response(mock_post)

        if api_response1 and api_response2:
            return True
        else:
            if not api_response1:
                print("Test llm API response type is wrong")
            if not api_response2:
                print("LLM_eval llm API response type is wrong")
            return False