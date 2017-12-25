# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import requests, os, time
from contextlib import closing
from bs4 import BeautifulSoup

ORIGINAL_URL = 'http://www.42soso.com'


class VideoSpider(object):

    def  __init__(self):
        self.__video_url__ = []

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                content = resp.content.decode('gbk')
            except Exception:
                content = resp.content.decode('utf-8')
        print(content)
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

    # 爬虫开始爬取
    def start_spider(self):
        print('开始下载')
        time_start = time.time()
        html_links = self.__get_htmlLinks__(ORIGINAL_URL)
        print(html_links)
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
        print('下载完成')
        print('共耗时', time.time()-time_start)

if __name__ == '__main__':

    videoSpider = VideoSpider()
    videoSpider.start_spider()