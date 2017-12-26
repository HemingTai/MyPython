# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import requests, os, time, sys
from contextlib import closing
from bs4 import BeautifulSoup
from FurtherLearning.Utility import *


ORIGINAL_URL = 'http://www.42soso.com'

class VideoSpider(object):

    def  __init__(self):
        self.__videoLinks__ = []

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        print(url)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                try:
                    content = resp.content.decode('gbk', errors='ignore')
                except Exception:
                    print('decode error url:',url)
                    # 防止字符超出gbk编码，所以选用gb18030并忽略解码过程中的错误
                    content = resp.content.decode('gb18030', errors='ignore')
                return content
        except Exception:
            print('request error url:', url)
            # 保存数据至文件
            self.__save_data__()

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
        self.__parse_videoLinks__(html_content)

    # 解析video的下载链接
    def __parse_videoLinks__(self,html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        all_div = soup.find_all('div', class_='shadow')
        for div in all_div:
            a = div.find('a')
            # 如果该链接是视频下载地址，则添加
            if a['href'] != 'http://jin.7557727.com:88/411316.html':
                # item = {'title':a['title'], 'url':ORIGINAL_URL+a['href']}
                item = '<p><a href="%s">%s</a></p>' %(ORIGINAL_URL+a['href'], a['title'])
                self.__videoLinks__.append(item)
        # 找到下一页的链接
        div_nextPage = soup.find('div', class_='page')
        #.contents属性表示该标签下所有的子标签并以列表形式返回
        all_a = div_nextPage.contents
        if len(all_a) > 0:
            nextPage_url = ORIGINAL_URL+all_a[-1]['href']
            # if nextPage_url != 'http://www.42soso.com/diao/se57_101.html':
            self.__get_videoLinks__(nextPage_url)

    # 保存数据至文件
    def __save_data__(self):
        print('开始写入文件...')
        if len(self.__videoLinks__):
            data = '<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<title>Videos</title>\n</head>\n<body>' + '\n'.join(
                self.__videoLinks__) + '\n</body>\n</html>'
            saveFile(SAVE_PATH, data)
        print('写入文件完成...')

    # 爬虫开始爬取
    def start_spider(self):
        time_start = time.time()
        print('开始解析原始网页...')
        html_links = self.__get_htmlLinks__(ORIGINAL_URL)
        print('获取视频下载链接...')
        self.__get_videoLinks__(html_links[9]) # html_links[9]
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
        print('获取视频链接完成...')
        time_end = time.time()
        print('共耗时', time_end - time_start)
        self.__save_data__()
        print('共耗时', time.time()-time_end)

if __name__ == '__main__':
    # 设置系统递归深度为100万，由于在解析视频连接时会找到下一页，然后不停的递归调用继续解析视频链接，所以要设置一下
    sys.setrecursionlimit(1000000)
    videoSpider = VideoSpider()
    videoSpider.start_spider()