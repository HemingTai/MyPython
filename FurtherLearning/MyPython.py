# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author = 'Hem1ng'


import requests, base64, json
from Crypto.Cipher import AES

# 网易云音乐某歌曲的热门评论
class Music163Spider(object):

    def __init__(self):
        self.__headers__ = {
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
    def __getHTMLContent__(self, url, limit, page):
        finalUrl = (url+'?limit=%s&offset=%s') % (limit, (page-1)*20)
        resp = requests.get(finalUrl, headers=self.__headers__)
        jsonData = resp.json()
        print(jsonData)
        # print(jsonData['comments'])
        # print(jsonData['total'])

    # 开始爬取
    def startSpider(self, url, limit, page):
        self.__getHTMLContent__(url, limit, page)

if __name__ == '__main__':
    spider = Music163Spider()
    spider.startSpider("http://music.163.com/api/v1/resource/comments/R_SO_4_436514312", 20, 1)