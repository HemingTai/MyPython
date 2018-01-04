#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


import requests

all_goods = []
tb_userid = '760703674'
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

# 获取淘宝userid：760703674
def get_tb_userid(url):
    response = requests.get(url)
    if response.status_code == 200:
        a = response.content.decode('utf-8')
        print(a)

def switch_rent(url):
    response = requests.get(url)
    if response.status_code == 200:
        a = response.content.decode('utf-8')
        print(a)



# for i in range(533):
#     print('爬取第%s页' % (i+1))
#     url = 'http://www.yishoudan.com/all/index/pname/page/aname/page/p/%s?json=1&version=2' % (i + 1)
#     get_allgoods(url)
# print(len(all_goods))
# get_tb_userid('https://oauth.taobao.com/authorize?response_type=code&client_id=23590390&redirect_uri=http://web.yishoudan.com/?m=otherUser&view=web&state=common')
switch_rent('http://api.yishoudan.com/newapi/gysq/760703674/1031429489/554949021645/556073549962/pid')