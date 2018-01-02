# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imgUrl    = scrapy.Field() # 图片链接
    title     = scrapy.Field() # 标题
    time      = scrapy.Field() # 时间
    brief     = scrapy.Field() # 摘要
    detailUrl = scrapy.Field() # 详情链接

class VideoItem(scrapy.Item):
    videoUrl   = scrapy.Field() # 视频链接
    videoTitle = scrapy.Field() # 视频标题

class ImageItem(scrapy.Item):
    imageUrl   = scrapy.Field() # 图片链接