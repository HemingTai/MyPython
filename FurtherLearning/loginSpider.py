# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, requests
from bs4 import BeautifulSoup
from PIL import Image

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

    def startCrawl(self):
        self.__getLoginHtml__()

class DoubanSpider(object):

    def __init__(self):
        self.__url__ = 'https://www.douban.com/accounts/login'
        self.__headers__ = {}
        self.__data__ = {}

    def __get_header__(self):
        self.__headers__['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/63.0.3239.84 Safari/537.36'
        self.__headers__['Referer'] = 'https://www.douban.com'
        self.__headers__['Host'] = 'www.douban.com'

    def __get_data__(self):
        self.__data__['source'] = 'index_nav'
        self.__data__['form_email'] = '964085993@qq.com'
        self.__data__['form_password'] = '***替换密码***'
        self.__data__['remember'] = 'on'

    def __login__(self):
        session = requests.session()
        resp = session.post(self.__url__, data=self.__data__, headers=self.__headers__)
        print(session.cookies)
        if resp.status_code == 200:
            result = session.get('https://www.douban.com/people/59490556/')
            print(result.content.decode('utf-8'))

    def start_crawl(self):
        self.__login__()

if __name__ == '__main__':

    # spider = LoginSpider()
    # spider.startCrawl()
    spider = DoubanSpider()
    spider.start_crawl()



