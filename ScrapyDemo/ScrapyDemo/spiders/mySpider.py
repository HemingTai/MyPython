#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule,CrawlSpider
from ..items import *
from bs4 import BeautifulSoup

class NewsSpider(scrapy.Spider):

    name = 'ITNews'
    allowed_domains = ['ithome.com']
    start_urls = ['https://www.ithome.com/blog/']

    def parse(self, response):
        print('bbbbb')
        # *********** 使用xpath解析 **************
        sel = scrapy.Selector(response)
        # xpath返回的是一个列表
        news_imgUrl    = sel.xpath('//a[@class="list_thumbnail"]/img/@src').extract()
        news_title     = sel.xpath('//div[@class="block"]/h2/a/text()|//div[@class="block"]/h2/a/font/text()').extract()
        news_time      = sel.xpath('//div[@class="block"]/h2/span/text()').extract()
        news_brief     = sel.xpath('//div[@class="memo"]/p/text()').extract()
        news_detailUrl = sel.xpath('//a[@class="list_thumbnail"]/@href').extract()

        # *********** 使用bs解析 *****************
        # soup = BeautifulSoup(response.text, 'lxml')
        # news_imgUrl    = [a.find('img')['src'] for a in soup.find_all('a',class_='list_thumbnail')]
        # news_detailUrl = [a['href'] for a in soup.find_all('a', class_='list_thumbnail')]
        # news_title     = [div.find('h2').find('a').string for div in soup.find_all('div', class_='block')]
        # news_time      = [div.find('h2').find('span').string for div in soup.find_all('div', class_='block')]
        # news_brief     = [div.find('p').string for div in soup.find_all('div', class_='memo')]

        for i in range(len(news_imgUrl)):
            print(i)
            item = NewsItem()
            item['imgUrl']    = 'https:'+news_imgUrl[i]
            item['title']     = news_title[i]
            item['time']      = news_time[i]
            item['brief']     = news_brief[i]
            item['detailUrl'] = news_detailUrl[i]
            yield item

# class ImageSpider(scrapy.Spider):
#
#     name = 'Image'
#     start_urls = ['http://desk.zol.com.cn/youxi/yingxionglianmeng/',
#                   'http://desk.zol.com.cn/youxi/yingxionglianmeng/2.html']
#
#     def parse(self, response):
#         sel = scrapy.Selector(response)
#         url_host = 'http://desk.zol.com.cn'
#         page_urls = sel.xpath('//li[@class="photo-list-padding"]/a/@href').extract()
#         for url in page_urls:
#             yield Request(url_host+url,callback=self.get_downloadLinkOfImage)
#
#     def get_downloadLinkOfImage(self, response):
#         sel = scrapy.Selector(response)
#         image_url = sel.xpath('//img[@id="bigImg"]/@src').extract()
#         item = ImageItem()
#         item['imageUrl'] = image_url[0]
#         yield item
#         next_url = sel.xpath('//a[@id="pageNext"]/@href').extract()
#         url_host = 'http://desk.zol.com.cn'
#         if next_url[0] != 'javascript:;':
#             yield Request(url_host+next_url[0], callback=self.get_downloadLinkOfImage)

class ImageSpider(CrawlSpider):

    name = 'Image'
    start_urls = ['https://movie.douban.com/photos/photo/2509298725']
    rules = (Rule(LinkExtractor(allow=(r'https://movie.douban.com/photos/photo/\d+')), callback='parse',follow=True),)

    def parse(self, response):
        sel = scrapy.Selector(response)
        image_url = sel.xpath('//div[@class="photo-wp"]/a[@class="mainphoto"]/img/@src').extract()
        if len(image_url):
            item = ImageItem()
            item['imageUrl'] = image_url[0]
            yield item


class VideoSpider(scrapy.Spider):

    name = 'Video'

    start_urls = ['http://www.42soso.com/diao/se57.html']

    def parse(self, response):
        sel = scrapy.Selector(response)
        url_host = 'http://www.42soso.com'
        video_url = sel.xpath('//div[@class="shadow"]/a/@href').extract()
        video_title = sel.xpath('//div[@class="shadow"]/a/@title').extract()
        for i in range(len(video_url)):
            if '/video/' in video_url[i]:
                item = VideoItem()
                item['videoUrl'] = url_host+video_url[i]
                item['videoTitle'] = video_title[i]
                yield item
            else:
                video_title.pop(i)

