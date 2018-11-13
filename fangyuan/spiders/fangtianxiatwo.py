# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import FangtianxiaTwoItem


class FangtianxiatwoSpider(scrapy.Spider):
    name = 'fangtianxiatwo'
    allowed_domains = ['sz.esf.fang.com']
    start_urls = ['http://sz.esf.fang.com/']

    custom_settings = {
        'LOG_FILE': 'log_fangtianxiatwo.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='#list_D02_10 > ul')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            self.logger.debug(link)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='li.area_sq > ul')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            self.logger.debug(link)
            yield Request(link.url, callback=self.parse_hall)

    def parse_hall(self, response):
        print('parse_hall response.url:' + response.url)
        self.logger.debug('parse_hall response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='#list_D02_12 > ul')
        print('3' * 80)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            self.logger.debug(link)
            yield Request(link.url, callback=self.parse_list)

    # def parse_area(self, response):
    #     print('parse_area response.url:' + response.url)
    #     self.logger.debug('parse_area response.url:' + response.url)
    #     yield Request(response.url, callback=self.parse_list)
    #     le = LinkExtractor(restrict_css='#list_D02_13 > ul')
    #     print('4' * 160)
    #     for link in le.extract_links(response):
    #         print(link, link.url, link.text)
    #         self.logger.debug(link, link.url, link.text)
    #         yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = FangtianxiaTwoItem()

        dl = response.css('.shop_list.shop_list_4>dl[id]')
        for i in dl:
            item['title'] = i.css('.tit_shop::text').extract_first().strip()
            item['url'] = 'http://esf.sz.fang.com' + i.css('h4 a::attr(href)').extract_first()
            item['total_price'] = float(i.css('.red>b::text').extract_first())
            item['unit_price'] = int(i.css('.price_right > span:nth-child(2)::text').re_first(r'[1-9]\d*|0'))
            if i.css('.floatl img[src2]'):
                item['img'] = i.css('.floatl img::attr(src2)').extract_first()
            else:
                item['img'] = i.css('.floatl img::attr(src)').extract_first()
            desc = i.css('p.tel_shop::text').extract()
            item['layout'] = desc[0].strip()
            item['area'] = re.search(r'[1-9]\d*', desc[1].strip())[0]
            item['floor'] = desc[2].strip()
            if len(desc) == 6:
                item['orientation'] = desc[3].strip()
                item['build_year'] = desc[4].strip()
            elif len(desc) > 3:
                item['orientation'] = ''
                item['build_year'] = desc[3].strip()
            item['community'] = i.css('.add_shop a::text').extract_first().strip()
            addr = i.css('.add_shop span::text').extract_first().split('-')
            print('addr :', addr)
            self.logger.debug('addr :' + str(addr))
            item['location'] = addr[0].strip()
            item['address'] = addr[1].strip()
            item['distance'] = i.css('.bg_none.icon_dt::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('.')[0]
            yield item

        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            next_url = 'http://sz.esf.fang.com' + next_page[0]
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(url=next_url, callback=self.parse_list)
