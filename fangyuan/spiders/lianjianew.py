# -*- coding: utf-8 -*-
import math

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import LianjiaNewItem


class LianjianewSpider(scrapy.Spider):
    name = 'lianjianew'
    allowed_domains = ['sz.fang.lianjia.com']
    start_urls = ['https://sz.fang.lianjia.com/loupan/']
    custom_settings = {
        'LOG_FILE': 'log_lianjianew.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_first)
        print('1' * 20)
        areas = response.css('div.filter-by-area-container > ul>li::attr(data-district-spell)').extract()
        for area in areas:
            url = 'https://sz.fang.lianjia.com/loupan/' + area
            print('url:', url)
            self.logger.debug('url:' + url)
            yield Request(url, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.page-box'):
            maxpage = math.ceil(float(response.css('.page-box::attr(data-total-count)').extract_first()) / 10)
        else:
            print('maxpage in else: {}'.format(maxpage))
            self.logger.debug('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: {}'.format(maxpage))
        print('response.url: {}'.format(response.url))
        self.logger.debug('response.url: {}'.format(response.url))
        for i in range(1, maxpage + 1):
            url = response.url + 'pg' + str(i)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = LianjiaNewItem()

        items = response.css('ul.resblock-list-wrapper > li[data-project-name]')
        for i in items:
            item['title'] = i.css('.resblock-name a::text').extract_first()
            item['url'] = 'https://sz.fang.lianjia.com' + i.css('.resblock-name a::attr(href)').extract_first()
            item['type'] = i.css('.resblock-type::text').extract_first()
            item['status'] = i.css('.sale-status::text').extract_first()
            item['total_price'] = i.css('.second::text').extract_first()
            item['unit_price'] = i.css('.number::text').extract_first()
            item['img'] = i.css('.lj-lazy::attr(data-original)').extract_first()
            item['area'] = i.css('.resblock-area span::text').extract_first()
            item['location'] = i.css('div.resblock-location > span:nth-child(1)::text').extract_first()
            item['community'] = i.css('div.resblock-location > span:nth-child(3)::text').extract_first()
            item['address'] = i.css('div.resblock-location > a::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-2].split('_')[-1]
            yield item

