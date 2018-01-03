#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


import requests

all_goods = []

def get_allgoods(url):
    response = requests.get(url)
    if response.status_code == 200:
        a = response.text
        if 'null' in response.text:
            a = a.replace('null', '"null"')
        data = eval(a)
        items = data['items']
        all_goods.append(items)
        print('爬取结束...')


for i in range(533):
    print('爬取第%s页' % (i+1))
    url = 'http://www.yishoudan.com/all/index/pname/page/aname/page/p/%s?json=1&version=2' % (i + 1)
    get_allgoods(url)
print(len(all_goods))