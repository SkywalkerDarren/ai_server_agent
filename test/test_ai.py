import unittest

from ai_service.ai import AI


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_ai(self):
        content = "你好"
        ai = AI()
        response = await ai.chat(content)
        print(response)


if __name__ == '__main__':
    unittest.main()
