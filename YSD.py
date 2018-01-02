#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


import requests

def get_allgoods(url):
    resp = requests.get(url)
    print(resp.text)

get_allgoods('http://www.yishoudan.com/index/index?json=1&version=2')