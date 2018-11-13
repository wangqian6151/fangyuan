# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import TongchengTwoItem


class TongchengtwoSpider(scrapy.Spider):
    name = 'tongchengtwo'
    allowed_domains = ['sz.58.com']
    start_urls = ['http://sz.58.com/ershoufang/']

    custom_settings = {
        'LOG_FILE': 'log_tongchengtwo.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='#qySelectFirst')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='#qySelectSecond')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_hall)

    def parse_hall(self, response):
        print('parse_hall response.url:' + response.url)
        self.logger.debug('parse_hall response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.filter-wrap > dl:nth-child(4) > dd')
        print('3' * 80)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_price)

    def parse_price(self, response):
        print('parse_price response.url:' + response.url)
        self.logger.debug('parse_price response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.filter-wrap > dl:nth-child(2) > dd')
        print('4' * 160)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = TongchengTwoItem()

        li = response.css('.house-list-wrap>li')
        for i in li:
            item['title'] = i.css('.title a::text').extract_first().strip()
            item['url'] = i.css('.title a::attr(href)').extract_first()
            item['total_price'] = float(i.css('.sum b::text').extract_first())
            item['unit_price'] = int(i.css('.unit::text').re_first(r'[1-9]\d*|0'))
            item['time'] = i.css('.time::text').extract_first()
            item['img'] = i.css('img::attr(data-src)').extract_first()
            item['layout'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(1)::text').extract_first().strip()
            print('parse_list area:' + i.css('div.list-info > p:nth-child(2) > span:nth-child(2)::text').extract_first())
            self.logger.debug('parse_list area:' + i.css('div.list-info > p:nth-child(2) > span:nth-child(2)::text').extract_first())
            item['area'] = float(i.css('div.list-info > p:nth-child(2) > span:nth-child(2)::text').re_first('[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0'))
            item['orientation'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(3)::text').extract_first()
            item['floor'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(4)::text').extract_first()
            item['community'] = i.css('div.list-info > p:nth-child(3) > span:nth-child(1) > a:nth-child(1)::text').extract_first()
            item['district'] = i.css('div.list-info > p:nth-child(3) > span:nth-child(1) > a:nth-child(2)::text').extract_first()
            if i.css('div.list-info > p:nth-child(3) > span:nth-child(1) > a:nth-child(3)::text'):
                item['location'] = i.css('div.list-info > p:nth-child(3) > span:nth-child(1) > a:nth-child(3)::text').extract_first()
            else:
                item['location'] = ''
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('.')[0]
            yield item

        le = LinkExtractor(restrict_css='div.pager > a.next')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)
