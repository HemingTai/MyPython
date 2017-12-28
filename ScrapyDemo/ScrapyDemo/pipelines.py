# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json, codecs, sys

class NewsPipeline(object):

    def __init__(self):
        self.file = codecs.open('IT_News.json', 'wb', 'utf-8')

    def process_item(self, item, spider):
        line = 'the news list:\n'

        for i in range(len(item['imgUrl'])):
            news_imgUrl = {'news_imgUrl':item['imgUrl'][i]}
            news_title = {'news_title':item['title'][i]}
            news_time = {'news_time': item['time'][i]}
            news_brief = {'news_brief': item['brief'][i]}
            news_detailUrl = {'news_detailUrl': item['detailUrl'][i]}
            line = line + json.dumps(news_imgUrl,ensure_ascii=False)
            line = line + json.dumps(news_title, ensure_ascii=False)
            line = line + json.dumps(news_time, ensure_ascii=False)
            line = line + json.dumps(news_brief, ensure_ascii=False)
            line = line + json.dumps(news_detailUrl, ensure_ascii=False)
        line = line + '\n'

        self.file.write(line)

    def close_spider(self, spider):
        self.file.close()
