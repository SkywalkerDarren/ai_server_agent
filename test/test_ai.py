import unittest
from unittest.mock import AsyncMock

from ai_service.ai import AI


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_ai(self):
        content = "查看下我当前的服务器占用"
        mock_message_service = AsyncMock()
        mock_ali_client = AsyncMock()

        mock_message_service.get_system_info.return_value = {
            "cpu": "99",
            "memory": "99",
        }

        ai = AI(mock_message_service, mock_ali_client)
        response = await ai.chat(content)
        print(response)


if __name__ == '__main__':
    unittest.main()
