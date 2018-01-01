# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import time, sys
from bs4 import BeautifulSoup
from functools import partial
from FurtherLearning.Utility import *
from multiprocessing.pool import Pool


ORIGINAL_URL = 'http://www.42soso.com'

class VideoSpider(object):

    def  __init__(self):
        self.__videoLinks__ = []
        self.__downloadLinks__ = []
        self.__saveLinks__ = []

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
            # saveDataToDatabase(self.__saveLinks__)

    # 获取所有html页面链接
    def __get_htmlLinks__(self, url):
        html_content = self.__get_htmlContent__(url)
        soup = BeautifulSoup(html_content, 'lxml')
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
        soup = BeautifulSoup(html_content, 'lxml')
        all_div = soup.find_all('div', class_='shadow')
        for div in all_div:
            a = div.find('a')
            # 如果该链接是视频下载地址，则添加
            if '/video/' in a['href']:
                self.__get_downloadLink__(ORIGINAL_URL + a['href'])
                # return
        # 找到下一页的链接
        a_nextPage = soup.find('a', string='下一页')
        if a_nextPage.get('href', None) != None:
            nextPage_url = ORIGINAL_URL + a_nextPage['href']
            if nextPage_url == 'http://www.42soso.com/diao/se57_5.html':
                return
            self.__get_videoLinks__(nextPage_url)

    # 获取视频下载链接
    def __get_downloadLink__(self, url):
        html_content = self.__get_htmlContent__(url)
        soup = BeautifulSoup(html_content, 'lxml')
        div = soup.find('div', class_='player').find('div', class_='a1')
        source = soup.find('source')
        self.__videoLinks__.append('<p><a href="%s" target="_blank">%s</a></p>' %(source['src'], div.string.strip()))
        self.__downloadLinks__.append(source['src'])
        self.__saveLinks__.append({'title':div.string.strip(), 'url':source['src']})

    # 保存数据至文件
    def __save_data__(self):
        print('开始写入文件...')
        if len(self.__videoLinks__):
            data = '<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<title>Videos</title>\n</head>\n<body>\n\t' + '\n\t'.join(self.__videoLinks__) + '\n</body>\n</html>'
            # data写入文件如果是文本必须是str,不能是list，dict
            saveFile(SAVE_PATH, data)
        print('写入文件完成...')

    # 下载视频
    def __download_video__(self):
        download = partial(downloadVideo)
        with Pool(2) as p:
            p.map(download, self.__downloadLinks__)

    # 爬虫开始爬取
    def start_spider(self):
        time_start = time.time()
        print('开始解析原始网页...')
        html_links = self.__get_htmlLinks__(ORIGINAL_URL)
        print('获取视频下载链接...')
        self.__get_videoLinks__('http://www.42soso.com/diao/se57_4.html') # html_links[9]
        print('获取视频下载链接完成...')
        time_end = time.time()
        print('共耗时', '%.f' % (time_end - time_start))
        self.__save_data__()
        print('开始写入数据...')
        # saveDataToDatabase(self.__saveLinks__)
        print('写入数据完成...')
        print('共耗时', '%.f' % (time.time()-time_end))
        print('开始下载视频...')
        setFileDownloadPath(DOWNLOAD_PATH)
        self.__download_video__()
        print('下载视频结束...')

if __name__ == '__main__':
    # 设置系统递归深度为100万，由于在解析视频连接时会找到下一页，然后不停的递归调用继续解析视频链接，所以要设置一下
    sys.setrecursionlimit(1000000)
    videoSpider = VideoSpider()
    videoSpider.start_spider()