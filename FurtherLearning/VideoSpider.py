# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import requests, os, time
from contextlib import closing
from bs4 import BeautifulSoup

ORIGINAL_URL = 'http://www.42soso.com'

class VideoSpider(object):

    def  __init__(self):
        self.__videoLinks__ = []

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                content = resp.content.decode('gbk', errors='ignore')
            except Exception:
                print(url)
                content = resp.content.decode('gb18030', errors='ignore')
            return content

    # 获取所有html页面链接
    def __get_htmlLinks__(self, url):
        html_content = self.__get_htmlContent__(url)
        html_links = self.__parse_htmlLinks__(html_content)
        return html_links

    # 解析html网页内容以获取网页链接
    def __parse_htmlLinks__(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'lxml')
        all_div = soup.find_all('div', class_='buttons2')
        html_links = []
        for div in all_div:
            all_a = div.find_all('a')
            for a in all_a:
                html_links.append(ORIGINAL_URL+a['href'])
        return html_links

    # 获取所有video链接
    def __get_videoLinks__(self, url):
        html_content = self.__get_htmlContent__(url)
        print(html_content)
        # self.__parse_videoLinks__(html_content)

    # 解析video的下载链接
    def __parse_videoLinks__(self,html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        all_div = soup.find_all('div', class_='shadow')
        for div in all_div:
            a = div.find('a')
            # 如果该链接是视频下载地址，则添加
            if a['href'] != 'http://jin.7557727.com:88/411316.html':
                item = {'title':a['title'], 'url':ORIGINAL_URL+a['href']}
                self.__videoLinks__.append(item)
        # 找到下一页的链接
        div_nextPage = soup.find('div', class_='page')
        #.contents属性表示该标签下所有的子标签并以列表形式返回
        all_a = div_nextPage.contents
        if len(all_a) > 0:
            nextPage_url = ORIGINAL_URL+all_a[-1]['href']
            self.__get_videoLinks__(nextPage_url)

    # 爬虫开始爬取
    def start_spider(self):
        time_start = time.time()
        print('开始解析原始网页...')
        html_links = self.__get_htmlLinks__(ORIGINAL_URL)
        print('获取视频下载链接...')
        self.__get_videoLinks__('http://www.42soso.com/diao/se57_802.html') # html_links[9]
# with closing(requests.get(video_url, stream=True)) as r:
#     video_name = os.path.basename(video_url)
#     chunk_size = 1024*1024
#     content_size = int(r.headers['content-length'])
#     totalCount = 0
#     with open(video_name, 'wb') as f:
#         for data in r.iter_content(chunk_size=chunk_size):
#             f.write(data)
#             totalCount += len(data)
#             print('正在下载',totalCount / content_size)
        print(self.__videoLinks__)
        print('获取视频链接完成...')
        print('共耗时', time.time()-time_start)

if __name__ == '__main__':

    videoSpider = VideoSpider()
    videoSpider.start_spider()