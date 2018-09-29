# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Hem1ng'


import requests
from FurtherLearning.Utility import *

# 网易云音乐某歌曲的热门评论
class Music163Spider(object):

    def __init__(self):
        self.__headers = {
        'Referer': 'http://music.163.com/song?id=436514312',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept - Language': 'zh - CN, zh;q=0.9',
        'Accept - Encoding': 'gzip, deflate',
        'Cookie': '_iuqxldmzr_=32; _ntes_nnid=fa11723d346a566aba420a6cf6a1176a,1527143751593; _ntes_nuid=fa11723d346a566aba420a6cf6a1176a; __utmc=94650624; __utmz=94650624.1527143753.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_TID=Z7oTxRUykZ4%2BJXgLy%2FhAh4jHn%2B8sT9Mb; playerid=12490336; JSESSIONID-WYYY=hm004xZxKkACxcvrwG6dA7z7JOvhvud0p5Y2Rai6FUTVnGDscd5fpoSJyR551H24w2jtyp4VIjJBeN9%5CNcZ%2B0NnXV9I9qZDDCXJ0HZDooYjR2RWWCbTAWC6ARey6z96nxQXfekdlgXcGvTn%2Fl3TPxMT%2FDXIlPn%5CgBTxJS%2FzcM5IWZn38%3A1527213429086; __utma=94650624.213514955.1527143753.1527147771.1527211817.3; __utmb=94650624.1.10.1527211817',
        'Connection': 'keep - alive',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # 获取网页内容
    # -url 爬取地址
    # -limit 每页评论数
    # -page 第几页
    def __getHTMLContent(self, url, limit, page):
        finalUrl = (url+'?limit=%s&offset=%s') % (limit, (page-1)*20)
        resp = requests.get(finalUrl, headers=self.__headers)
        jsonData = resp.json()
        print(jsonData)
        # print(jsonData['comments'])
        # print(jsonData['total'])

    # 开始爬取
    def startSpider(self, url, limit, page):
        self.__getHTMLContent(url, limit, page)

# 今日头条
class TouTiaoSpider(object):
    def __init__(self):
        self.__header = {
            'referer': 'https://www.toutiao.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

    def __getHTMLContent(self, url):
        resp = requests.get(url, headers= self.__header)
        if resp.status_code == 200:
            print(resp.text)

    # 获取顶部滚动图片新闻
    def __getTopicContent(self):
        self.__getHTMLContent('https://www.toutiao.com/api/pc/focus/')

    # 获取搜索框热点
    def __getSearchContent(self):
        self.__getHTMLContent('https://www.toutiao.com/search/suggest/initial_page/')

    # 获取24小时热闻
    def __getRealTimeContent(self):
        self.__getHTMLContent('https://www.toutiao.com/api/pc/realtime_news/')

    # 获取精彩图片新闻
    def __getAmazingContent(self):
        self.__getHTMLContent('https://www.toutiao.com/api/pc/hot_gallery/?widen=1')

    # 获取全部新闻
    def __getNewsContent(self):
        self.__getHTMLContent('https://www.toutiao.com/api/pc/feed/?max_behot_time=1527746296&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1850B509FEA153&cp=5B0FCA7105731E1&_signature=-2kA6RAXoHBEH.EPZ20y2vtpAP')
                              # 'https://www.toutiao.com/api/pc/feed/?max_behot_time=1527743596&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1254B700FEA447&cp=5B0F2A4474474E1&_signature=-2kA6RAXoHBEH.EPZ23X9PtpAP'

    # 开始爬取
    def startSpider(self):
        self.__getTopicContent()
        self.__getSearchContent()
        self.__getRealTimeContent()
        self.__getAmazingContent()
        self.__getNewsContent()

# 淘女郎实体类
class TaoGirl(object):

    def __init__(self):
        self.isV = ''
        self.picUrl = ''
        self.nickName = ''
        self.tags = []
        self.userId = ''
        self.priceList = []
        self.homepage = ''
        self.titleArray = []
        self.fans = ''

    def __str__(self):
        return 'TaoGirl昵称：%s，id：%s，粉丝数：%s' % (self.nickName, self.userId, self.fans)

# 淘女郎
class TaoGirlSpider(object):
    def __init__(self):
        self.__header = {
            'Host': 'v.taobao.com',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'br, gzip, deflate',
            'Cookie': 'isg=BJOTxCmDzB5T3oBKabBNPZxoIBG9SCcKBW4nXUWw77LpxLNmzRi3WvGS-rSq_38C; uc1=cookie14=UoTfLJBJdZP4Dw%3D%3D; JSESSIONID=A7CF452EA922074309956007EA52150F; _tb_token_=e615b6e9763d7; cookie2=1447d3bd4a2f0c3bf48ec65437c699f9; t=07b79fe041e308c059701ec21f770ef3; v=0; cna=TkorFBSSgVgCAbSpkrnXzdjF',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
            'Referer': 'https://v.taobao.com/v/content/live?catetype=704&from=taonvlang',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.__girlsArray__ = []

    def __getHTMLContent(self, url):
        resp = requests.get(url, headers= self.__header)
        if resp.status_code == 200:
            a = resp.text[12:-2]
            a = a.replace('true', '"true"')
            a = a.replace('false', '"false"')
            result = eval(a)
            items = result['data']
            data = items['result']
            self.__getTaoGirls__(data)

    def __getTaoGirls__(self, itemArray):
        for item in itemArray:
            girl = TaoGirl()
            girl.isV = item['isV']
            girl.picUrl = item['picUrl']
            girl.nickName = item['nick']
            girl.tags = item['tag']
            girl.userId = item['userId']
            girl.priceList = item['priceList']
            girl.homepage = item['homeUrl']
            girl.titleArray = item['titleArray']
            girl.fans = item['fansCount']
            print(girl)
            self.__girlsArray__.append(girl)

    # 开始爬取
    def startSpider(self, url):
        for page in range(1,26):
            self.__getHTMLContent(url.format(page = page))
        saveTaoGirlsDataToDatabase(self.__girlsArray__)

if __name__ == '__main__':
    # spider = Music163Spider()
    # spider.startSpider("http://music.163.com/api/v1/resource/comments/R_SO_4_436514312", 20, 1)

    # ttSpider = TouTiaoSpider()
    # ttSpider.startSpider()

    spider = TaoGirlSpider()
    spider.startSpider("https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=704&currentPage={page}&_ksTS=1537508050015_73&callback=jsonp74")