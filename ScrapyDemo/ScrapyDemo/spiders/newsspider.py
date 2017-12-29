#!/usr/bin/env python3
#-*- coding: utf-8 -*-


__author__ = 'Hem1ng'


import scrapy
from ..items import NewsItem
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



