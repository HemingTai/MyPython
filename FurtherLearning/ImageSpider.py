# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import re, os, requests, time, queue, threading, selenium.webdriver as webdriver
from bs4 import BeautifulSoup



class ImageSpider(object):

    def __init__(self):
        self.__urlList__ = []

    # 获取所有图片的下载链接
    def __get_imageLinks__(self, url):
        htmlContent = self.__get_htmlContent__(url)
        print(htmlContent)

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.content.decode('gb2312')

    # 解析html网页内容
    def __parse_htmlContent__(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'lxml')
        ul = soup.find('ul', id='skinBG')
        all_img = ul.find_all('img')
        for img in all_img:
            print(img['src'])

    # 爬虫开始爬取
    def start_spider(self, url):
        self.__get_imageLinks__(url)




    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # ul = soup.find('ul', id='m-song-module')
    # all_li = ul.find_all('li')
    # datas = []
    # for li in all_li:
    #     album_img = li.find('img')['src']
    #     endpos = album_img.index('?')
    #     album_name = li.find('a',class_='tit s-fc0').string
    #     album_time = li.find('span').string
    #     datas.append({'img':album_img[:endpos],'name':album_name,'time':album_time})
    # imgDir = os.path.join(os.path.abspath('.'),'img')
    # makeDir(imgDir)
    # os.chdir(imgDir)
    # fileNames = os.listdir(imgDir) # 获取当前路径下所有文件及子文件夹的名字
    # 单线程下载图片
    # for item in datas:
    #     if item['time']+'-'+item['name']+'.jpg' in fileNames:
    #         print('图片已存在')
    #     else:
            # saveImg(item['img'],item['time']+'-'+item['name'])

    # 多线程下载图片
    # q = queue.Queue()
    # for urlItem in datas:
    #     q.put(urlItem['img'])
    # t = threading.Thread(target=downloadImage, args=(q,))
    # t.start()
    # t.join()

imgSpider = ImageSpider()
imgSpider.start_spider('http://lol.qq.com/web201310/info-defail.shtml?id=Thresh')