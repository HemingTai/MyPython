# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re

__author__ = 'Hem1ng'

'''
    豆瓣电影Top100爬虫
'''
class DouBanSpider(object):

    def __init__(self):
        self.__page__ = 1
        self.cur_url = 'https://movie.douban.com/top250?start={page}&filter='
        self.datas = []
        self.picLinks = []
        self._top_num = 1
        print('豆瓣电影爬虫准备就绪, 准备爬取数据...')

    # 获取当前页面内容
    def __getHTMLContent__(self, cur_page):
        url = self.cur_url
        my_page = (requests.get(url.format(page=(cur_page - 1)*25))).content.decode('utf-8')
        return my_page

    # 获取电影名称
    def __find_title__(self, my_page):
        temp_data = []
        # .*?是非贪婪模式匹配，一旦第一次匹配结束就不再往后继续匹配了
        # .*是贪婪模式匹配，第一次匹配结束继续往后匹配，直到字符串结束
        # re.S表示将.(表示除了换行符以外的所有字符)的作用扩展到整个字符串，包括换行符。
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find('&nbsp;') == -1:
                temp_data.append('Top'+str(self._top_num)+' '+item)
                self._top_num += 1
        self.datas.extend(temp_data)

    # 获取电影的缩略图链接
    def __find_picLinks__(self, my_page):
        movie_picLinks = re.findall(r'<img width="100" alt=.*?src=(.*?)class="">', my_page, re.S)
        for index, link in enumerate(movie_picLinks):
            self.picLinks.append(link)

    # 爬虫入口
    def start_spider(self):
        while self.__page__ <= 4:
            my_page = self.__getHTMLContent__(self.__page__)
            self.__find_title__(my_page)
            self.__find_picLinks__(my_page)
            self.__page__ += 1

'''
    豆瓣上关于《猎场》的前100条热门影评
'''
class ReviewSpider(object):

    def __init__(self):
        self.__page__ = 0
        self.__resp_page__ = 0
        self.__reviews__ = []
        self.__pageUrl__ = 'https://movie.douban.com/subject/26322642/discussion/?start={page}&sort_by=vote'
        self.__respUrl__ = '{hostUrl}?start={respPage}&author=0#comments'

    # 获取热门影评页面内容
    def __getHTMLContent__(self, cur_page):
        url = self.__pageUrl__.format(page=cur_page*20)
        response = requests.get(url)
        page = response.content.decode('utf-8')
        return page

    # 获取热门影评标题和链接
    def __getReviewLinkAndTitle__(self, content):
        temp_data = re.findall(r'<a.*?href="(.*?)".*?title="(.*?)".*?class="">', content, re.S)
        for item in temp_data:
            self.__reviews__.append({'title':item[1],'url':item[0]})

    def __getResponsePageNumber__(self, content):
        print('************')
        temp_data = re.findall(r'<a href=".*" >(\d+)</a>', content, re.S)
        print(temp_data)
        print('############')

    # 获取影评和回复页面内容
    def __getResponseContent__(self, hostUrl, cur_page):
        url = self.__respUrl__.format(hostUrl=hostUrl, respPage=cur_page * 100)
        response = requests.get(url)
        page = response.content.decode('utf-8')
        return page

    def __getResponse__(self, reviewLink):
        resp = self.__getResponseContent__(reviewLink, self.__resp_page__)
        self.__getResponsePageNumber__(resp)




    def start_spider(self):
        # while self.__page__ < 5:
        #     content = self.__getHTMLContent__(self.__page__)
        #     self.__getReviewLinkAndTitle__(content)
        #     self.__page__ += 1
        self.__getResponse__('https://movie.douban.com/subject/26322642/discussion/615091946/')




if __name__ == '__main__':
    # ************** 电影Top100 *************** #
    # mySpider = DouBanSpider()
    # mySpider.start_spider()
    # for item in mySpider.datas:
    #     print(item)
    # print('豆瓣爬虫爬取结束...')

    # **************《猎场热门影评》*************** #
    reviewSpider = ReviewSpider()
    reviewSpider.start_spider()
