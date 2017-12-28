#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


from scrapy.selector import Selector
from scrapy.spiders import Spider
from ..items import NewsItem

class NewsSpider(Spider):
    name = 'ITNews'
    allowed_domains = ['www.ithome.com']
    start_url = ['https://www.ithome.com/blog/']

    def parse(self, response):
        sel = Selector(response)

        # Selector返回的是一个列表
        news_imgUrl    = sel.xpath('//a[@class="list_thumbnail"]/img/@src').extract()
        news_title     = sel.xpath('//div[@class="block"]/h2/a/text()').extract()
        news_time      = sel.xpath('//div[@class="block"]/h2/span/text()').extract()
        news_brief     = sel.xpath('//div[@class="memo"]/p/text()').extract()
        news_detailUrl = sel.xpath('//a[@class="list_thumbnail"]/@href').extract()

        item = NewsItem()
        item['imgUrl']    = [url.encode('utf-8') for url in news_imgUrl]
        item['title']     = [title for title in news_title]
        item['time']      = [time for time in news_time]
        item['brief']     = [brief for brief in news_brief]
        item['detailUrl'] = [url.encode('utf-8') for url in news_detailUrl]
        yield item

        print(news_imgUrl,news_title,news_time,news_brief,news_detailUrl)



