# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from .items import *

class NewsPipeline(object):

    def __init__(self):
        self.file = open("news.json", "w")

    # 该方法在spider被开启时被调用
    def open_spider(self, spider):
        print('aaaaa')

    def process_item(self, item, spider):
        print('ccccc')
        # for i in range(len(item['title'])):
        #     newsItem = NewsItem()
        #     newsItem['imgUrl'] = item['imgUrl'][i]
        #     newsItem['title'] = item['title'][i]
        #     newsItem['time'] = item['time'][i]
        #     newsItem['brief'] = item['brief'][i]
        #     newsItem['detailUrl'] = item['detailUrl'][i]
        line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(line)

    # 该方法在spider被关闭时被调用
    def colse_spider(self, spider):
        print('ddddd')
        self.file.close()

class VideoPipeline(object):

    def __init__(self):
        self.file = open("video.json", "w")

    # 该方法在spider被开启时被调用
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(line)

    # 该方法在spider被关闭时被调用
    def colse_spider(self, spider):
        self.file.close()
