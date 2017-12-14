# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re

__author__ = 'Hem1ng'


class DouBanSpider(object):

    def __init__(self):
        self.page = 1
        self.cur_url = 'https://movie.douban.com/top250?start={page}&filter='
        self.datas = []
        self._top_num = 1
        print('豆瓣电影爬虫准备就绪, 准备爬取数据...')

    def get_page(self, cur_page):
        url = self.cur_url
        my_page = (requests.get(url.format(page=(cur_page - 1)*25))).content.decode('utf-8')
        return my_page

    def find_title(self, my_page):
        temp_data = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find('&nbsp;') == -1:
                temp_data.append('Top'+str(self._top_num)+' '+item)
                self._top_num += 1
        self.datas.extend(temp_data)

    def start_spider(self):
        while self.page <= 4:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1

if __name__ == '__main__':
    mySpider = DouBanSpider()
    mySpider.start_spider()
    for item in mySpider.datas:
        print(item)
    print('豆瓣爬虫爬取结束...')