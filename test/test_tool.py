import unittest

from ai_service.tools import StopGameTool


class MyTestCase(unittest.TestCase):
    def test_tool(self):
        s = StopGameTool(None).get_info()
        print(s)
        # stop_game = StopGameTool()
        # print(stop_game.tool_dict())


if __name__ == '__main__':
    unittest.main()
