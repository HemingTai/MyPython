# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Hem1ng'

import time, sys, logging
from bs4 import BeautifulSoup
from functools import partial
from FurtherLearning.Utility import *
from multiprocessing.pool import Pool

ORIGINAL_URL = 'http://www.zxxdz.com:8888/zxdz.html'


class VideoSpider(object):

    def __init__(self):
        self.__categoriesLinks__ = []
        self.__htmlLinks__ = []
        self.__videoLinks__ = []
        self.__pages__ = 0

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                try:
                    content = resp.content.decode('utf-8', errors='ignore')
                except Exception:
                    logging.error('decode error url:', url)
                return BeautifulSoup(content, 'lxml')
        except Exception:
            logging.error('request error url:', url)

    # 获取所有目录链接
    def __get_categoriesLinks__(self, url):
        logging.info('开始获取所有分类链接')
        soup = self.__get_htmlContent__(url)
        a_all = soup.find_all('a', class_='item')
        for a in a_all:
            self.__categoriesLinks__.append({a['title']: a['href']})
        logging.info('获取所有分类链接完成')
        self.__get_htmlLinks__()

    # 获取当前分类下所有页面链接
    def __get_htmlLinks__(self):
        for dic in self.__categoriesLinks__:
            for title, url in dic.items():
                logging.info('开始获取{title}分类下所有页面链接'.format(title=title))
                soup = self.__get_htmlContent__(url)
                li_last = soup.find('li', class_='last')
                if not li_last is None:
                    temp = li_last.find('a')['data-parameters']
                    self.__pages__ = int(temp[23:])
                    for page in range(1, self.__pages__ + 1):
                        self.__htmlLinks__.append({title: url + str(page)})
                else:
                    self.__pages__ = 1
                    self.__htmlLinks__.append({title: url})
                logging.info('获取{title}分类下所有页面链接完成，总页数为：{pages}'.format(title=title, pages=self.__pages__))
        self.__get_videoLinks__()

    # 获取所有video链接
    def __get_videoLinks__(self):
        logging.info('开始解析视频播放地址...')
        for dic in self.__htmlLinks__:
            for title, url in dic.items():
                soup = self.__get_htmlContent__(url)
                all_div = soup.find_all('div', class_='item')
                for div in all_div:
                    a = div.find('a')
                    self.__videoLinks__.append({a['title']: a['href']})
        logging.info('解析视频播放地址结束')
        print(self.__categoriesLinks__)
        print(self.__videoLinks__)
        logging.info('开始写入数据库...')
        saveVideoDataToDatabase(self.__videoLinks__)
        logging.info('写入数据库完成')

    # 爬虫开始爬取
    def start_spider(self):
        logging.info('爬虫开启')
        time_start = time.time()
        logging.info('开始解析网页')
        self.__get_categoriesLinks__(ORIGINAL_URL)
        logging.info('解析网页完成')
        time_end = time.time()
        logging.info('共耗时{time}s'.format(time=time_end - time_start))
        logging.info('爬虫结束')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # 设置系统递归深度为100万，由于在解析视频连接时会找到下一页，然后不停的递归调用继续解析视频链接，所以要设置一下
    sys.setrecursionlimit(1000000)
    videoSpider = VideoSpider()
    videoSpider.start_spider()
