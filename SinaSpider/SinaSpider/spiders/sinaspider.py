#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'

from scrapy.spiders import Spider, CrawlSpider, Request

class SinaSpider(Spider):

    name = 'Sina'
    user_id = '2678408783'
    start_urls = ['https://weibo.cn/%s/info' % user_id,]

    def parse(self, response):
        print(response.text)
