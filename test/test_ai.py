import unittest
from unittest.mock import AsyncMock

from ai_service.ai import AI
from search_service.search_client import SearchClient


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_ai(self):
        # content = "查看下我当前的服务器占用"
        content = "帮我查下今天的日期"
        mock_message_service = AsyncMock()
        mock_ali_client = AsyncMock()
        mock_search_service = AsyncMock()

        mock_message_service.get_system_info.return_value = {
            "cpu": "99",
            "memory": "99",
        }

        mock_search_service.search.return_value = '[{"title": "日历网", "href": "https://www.rili.com.cn/", "body": "日历网主要提供在线日历查询，农历、节日、节气等方面的内容。"}, {"title": "今日农历、农历查询、农历转阳历- 农历日历- 黄道吉日网", "href": "https://nongli.hdjr.org/", "body": "该网页提供了今日农历、农历查询、农历转阳历等功能，以及各种吉凶事宜的查询。您可以根据您的生辰八字，选择最适合您的吉日进行各种活动，如搬家、结婚、开业等。"}, {"title": "今日日历详情，今天日历查询，今日日历农历老黄历，今天 ...", "href": "https://rili.ximizi.com/jinririli.php", "body": "查询今天的公历、农历、回历、五行、执位、值日星神等信息，以及今天的时辰宜忌吉凶、岁次、胎神方位、吉神宜趋、凶煞厌对等。还可查询明日日历、月历、年历、节气、节日等。"}, {"title": "黄历_老黄历_今日黄历查询-黄历网", "href": "https://www.huangli.com/huangli/", "body": "黄历网为广大网友提供最准确的老黄历看日子，今日黄历内容包括了良辰吉日,在线算命，十二生肖运程、风水学，命相学、节气查询，节日查询等还有中国传统文化习俗，老黄历致力于做中国国内最实用，最方便，最准确的黄历查询."}, {"title": "万年日历查询 - 在线日历", "href": "https://wannianrili.bmcx.com/", "body": "查询今天的日期和节气，以及各种历法和节日的详细信息。输入日期，查看生肖、星座、彭祖百忌、胎神占方、年五行、星宿、日五行、节气、儒略日、伊斯兰历等。"}, {"title": "北京时间 - 真太阳时 - 日历", "href": "https://time.org.cn/", "body": "刷新时间. 点击日期查看详情，可写入备忘. 上月 年 月 FEB 下月 . 首页默认显示标准北京时间，可切换显示其他经度的平太阳时和真太阳时，时间精度一般在50毫秒之内。 日历包括农历、节气、干支、三九三伏、重要节日等信息。 日期上可写入临时记事。"}, {"title": "今日黄历_黄道吉日_万年历_黄历网", "href": "https://hli.cc/", "body": "今日黄历_黄道吉日_万年历_黄历网. 老黄历:2024年3月1日 农历2024年正月廿一. 公历/阳历 年 月 日. 黄历选择. 吉日选择. 2018年. 2019年. 2020年. 2021年. 2022年. 2023年. 2024年. 2025年. 2026年. 2027年. 2028年. 2029年. 2030年. 1 月. 2 月. 3 月. 4 月. 5 月. 6 月. 7 月. 8 月. 9 月. 10 月. 11 月. 12 月. 1日. 2日. 3日. 4日. 5日. 6日. 7日. 8日. 9日. 10日."}, {"title": "农历查询,今天是农历几号,今天是农历几月几日-天天农历网", "href": "https://www.ttnongli.com/jinri/", "body": "二零二四年正月二十三. 2024年3月3日 星期日. 今日是阳历3月3日，是黑道日. 今日是星期日，是工作日. 今日是虎日，冲生肖猴. 今日五行属木，是木日. 今日财神方位为西南方向. 今日喜神方位为正南方向. 今日偏财位为正西方向. 今日卦象是震卦（震为雷） 今日幸运数字是 1 、 6. 2024年农历正月二十三是全国爱耳日. 今日是双鱼座 ，上升星座是双子座."}, {"title": "【今天是农历几月几日】今天是什么日子_今天农历多少 ...", "href": "https://wannianli.tianqi.com/today", "body": "今天是2024年3月6日 星期三 第1周 今天是农历2024年1月26日 正月廿六"}, {"title": "今日黄历宜忌查询,今日老黄历,今天是什么日子老黄历_天天黄历", "href": "https://m.tthuangli.com/jinrihuangli/", "body": "今天黄历值神是天刑，是 黑道日. 今天是2024年的 63 天，距离全年结束还有 303 天. 今天是第 9 周,距离2024年结束还有 43 周. 今天是 全国爱耳日 , 距离下一个节日 （龙抬头） 还有 8天. 当前节气 （雨水） ，距离下一个节气 （惊蛰） 还有 2天. 上一节气：雨水. 2024年2月19日 12:12:58. 下一节气：惊蛰. 2024年3月5日 10:22:31. 生肖. 虎. 五行. 火. 第几周. 第9周. 纳音. 炉中火. 冲煞. 冲猴煞北. 星座. 双鱼座. 喜神. 正南. 财神. 西南. 福神."}]'

        ai = AI(mock_message_service, mock_ali_client, mock_search_service)
        response = await ai.chat(content)
        print(response)


if __name__ == '__main__':
    unittest.main()
