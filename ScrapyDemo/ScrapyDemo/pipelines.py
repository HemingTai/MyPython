# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json, mysql.connector
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
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
            raise DropItem('下载失败 %s' % image_path)
        else:
            print('下载成功...')

class VideoPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        print('开始下载...')
        yield Request(item['videoUrl'])

    # results是一个list,里面只有一个元素是tuple类型，tuple里面有两个值，第一个是布尔值，第二个是dict
    # dict里面有三个键值对,一个是url，一个是path，一个是checksum
    def item_completed(self, results, item, info):
        video_path = [x['path'] for ok,x in results if ok]
        if not video_path:
            raise DropItem('下载失败 %s' % video_path)
        else:
            print('下载成功...')

class YSDPipeline(object):

    def __init__(self):
        self.file = open("goods.json", "w+")
        # self.conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='99112911', database='Goods')
        # self.cur  = self.conn.cursor()

    # 该方法在spider开启时被调用
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        line = ''
        goods = item['goods']
        for i in range(len(goods)):
            line = line+json.dumps(goods[i])+'\n'
            # self.saveDatatoDB(goods[i])

        self.file.write(line)

    # 该方法在spider被关闭时被调用(？未发现被调用)
    def colse_spider(self, spider):
        # self.conn.commit()
        # self.cur.close()
        # self.conn.close()
        self.file.close()

    def saveDatatoDB(self,temp):
        self.cur.execute('insert into t_goods (num_iid, title) values (%s, %s)', (temp['num_iid'], temp['title']))