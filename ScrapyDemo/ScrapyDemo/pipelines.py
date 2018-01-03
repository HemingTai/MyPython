# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class NewsPipeline(object):

    def __init__(self):
        self.file = open("news.json", "w")

    # 该方法在spider被开启时被调用
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(line)

    # 该方法在spider被关闭时被调用(？未发现被调用)
    def colse_spider(self, spider):
        self.file.close()

class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(item['imageUrl'])

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem('图片下载失败 %s' % image_path)
        else:
            print('下载成功...')

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

class YSDPipeline(object):

    def __init__(self):
        self.file = open("goods.json", "w+")

    # 该方法在spider被开启时被调用
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        line = ''
        goods = item['goods']
        for i in range(len(goods)):
            line = line+json.dumps(goods[i])+'\n'
        self.file.write(line)

    # 该方法在spider被关闭时被调用(？未发现被调用)
    def colse_spider(self, spider):
        print('ccccccccccccc')
        self.file.close()