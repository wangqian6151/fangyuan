# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import LianjiaTwoItem


class LianjiatwoSpider(scrapy.Spider):
    name = 'lianjiatwo'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['https://sz.lianjia.com/ershoufang/']

    custom_settings = {
        'LOG_FILE': 'log_lianjiatwo.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_first)
        le = LinkExtractor(restrict_css='div[data-role="ershoufang"]')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list_first)
        le = LinkExtractor(restrict_css='div[data-role="ershoufang"] > div:nth-child(2)')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list_first)

    def parse_list_first(self, response):
        maxpage = 0
        if response.css('.house-lst-page-box'):
            maxpage = int(re.findall('"totalPage":(.*),"curPage"', response.text)[0])
        else:
            print('maxpage in else: {}'.format(maxpage))
            self.logger.debug('maxpage in else: {}'.format(maxpage))
        print('maxpage: {}'.format(maxpage))
        self.logger.debug('maxpage: {}'.format(maxpage))
        print('parse_list_first response.url: {}'.format(response.url))
        self.logger.debug('parse_list_first response.url: {}'.format(response.url))
        for i in range(1, maxpage + 1):
            url = response.url + 'pg' + str(i) + '/'
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = LianjiaTwoItem()

        li = response.css('.sellListContent>.clear.LOGCLICKDATA')
        for i in li:
            item['title'] = i.css('.title a::text').extract_first().strip()
            item['url'] = i.css('.title a::attr(href)').extract_first()
            item['total_price'] = float(i.css('.totalPrice span::text').extract_first())
            item['unit_price'] = int(i.css('.unitPrice span::text').re_first(r'[1-9]\d*|0'))
            item['img'] = i.css('.lj-lazy::attr(data-original)').extract_first()
            item['community'] = i.css('.address a::text').extract_first()
            desc = i.css('.houseInfo::text').extract_first().split('|')
            if len(desc) == 6:
                item['layout'] = desc[1].strip()
                item['area'] = re.findall(r'[1-9]\d*|0', desc[2].strip())[0]
                item['orientation'] = desc[3].strip()
                item['decoration'] = desc[4].strip()
                item['elevator'] = desc[5].strip()
            elif len(desc) == 5:
                item['layout'] = desc[1].strip()
                item['area'] = re.findall(r'[1-9]\d*|0', desc[2].strip())[0]
                item['orientation'] = desc[3].strip()
                item['decoration'] = desc[4].strip()
                item['elevator'] = ''
            item['floor'] = i.css('.positionInfo::text').extract_first().split('-')[0].strip()
            item['location'] = i.css('.positionInfo a::text').extract_first()
            num = i.css('.followInfo::text').extract_first().split('/')
            print('num:{}'.format(num))
            self.logger.debug('num:{}'.format(num))
            if num:
                item['focus_num'] = num[0].strip()
                item['watch_num'] = num[1].strip()
                item['pubdate'] = num[2].strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('.')[0]
            yield item
