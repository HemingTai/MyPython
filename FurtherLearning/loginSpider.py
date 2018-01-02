# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, requests, pytesseract
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

__author__ = 'Hem1ng'


class LoginSpider(object):

    def __init__(self):
        self.__url_login__ = 'https://accounts.douban.com/login'

    def __getLoginHtml__(self):
        resp = requests.get(self.__url_login__)
        self.__parseLoginHtml__(resp.content.decode('utf-8'))

    def __parseLoginHtml__(self, html):
        soup = BeautifulSoup(html,'lxml')
        captcha = soup.find('img', id='captcha_image')
        if captcha:
            print(captcha['src'])
            captcha_img = requests.get(captcha['src'])
            with open('1.png','wb') as f:
                f.write(captcha_img.content)
                f.flush()
                os.fsync(f.fileno())
        if os.path.isfile('1.png'):
            self.__image2text__()

    def __image2text__(self):
        img = Image.open('1.png')
        print(pytesseract.image_to_string(img,lang='eng'))

    def startCrawl(self):
        self.__getLoginHtml__()

if __name__ == '__main__':

    spider = LoginSpider()
    spider.startCrawl()


