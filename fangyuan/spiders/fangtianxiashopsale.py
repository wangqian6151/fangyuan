# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import FangtianxiaShopsaleItem


class FangtianxiashopsaleSpider(scrapy.Spider):
    name = 'fangtianxiashopsale'
    allowed_domains = ['sz.shop.fang.com']
    start_urls = ['http://sz.shop.fang.com']

    custom_settings = {
        'LOG_FILE': 'log_fangtianxiashopsale.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.screen_al > ul > li:nth-child(1) > ul')
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
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = FangtianxiaShopsaleItem()

        dl = response.css('.shop_list>dl[id]')
        for i in dl:
            item['title'] = i.css('.tit_shop::text').extract_first().strip()
            item['url'] = 'http://sz.shop.fang.com' + i.css('h4 a::attr(href)').extract_first()
            item['total_price'] = int(i.css('.red>b::text').extract_first())
            item['unit_price'] = float(i.css('dd.price_right > span:nth-child(2) > i::text ').extract_first())
            if i.css('.floatl img[src2]'):
                item['img'] = i.css('.floatl img::attr(src2)').extract_first()
            else:
                item['img'] = i.css('.floatl img::attr(src)').extract_first()
            item['area'] = int(i.css('span.color3 > b::text').extract_first())
            if i.css('.add_shop a::text').extract_first():
                item['community'] = i.css('.add_shop a::text').extract_first().strip()
            else:
                item['community'] = i.css('.add_shop::text').extract_first().strip()
            if '商铺' in item['community']:
                item['community'] = item['community'].replace('商铺', '')
            item['address'] = i.css('p.add_shop > span::text').extract_first().strip()
            desc = i.css('.tel_shop::text').extract()
            item['type'] = desc[0].split('：')[1].strip()
            item['floor'] = desc[1].split('：')[1].strip()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('.')[0]
            yield item

        le = LinkExtractor(restrict_css='#PageControl1_hlk_next')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)

