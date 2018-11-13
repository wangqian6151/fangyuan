# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import QfangTwoItem


class QfangtwoSpider(scrapy.Spider):
    name = 'qfangtwo'
    allowed_domains = ['shenzhen.qfang.com']
    start_urls = ['https://shenzhen.qfang.com/sale']

    custom_settings = {
        'LOG_FILE': 'log_qfangtwo.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.search-area-detail')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.search-area-second')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_hall)

    def parse_hall(self, response):
        print('parse_hall response.url:' + response.url)
        self.logger.debug('parse_hall response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.search-con-wrapper > div:nth-child(4) > ul')
        print('3' * 80)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = QfangTwoItem()

        items = response.css('#cycleListings>ul>li')
        for i in items:
            item['title'] = i.css('.house-title a::text').extract_first().strip()
            item['url'] = 'https://shenzhen.qfang.com' + i.css('.house-title a::attr(href)').extract_first()
            item['total_price'] = int(i.css('.sale-price::text').extract_first())
            item['unit_price'] = int(i.css('.show-price p::text').re_first(r'[1-9]\d*'))
            item['img'] = i.css('img::attr(data-original)').extract_first().strip()
            item['layout'] = i.css('p.house-about.clearfix > span:nth-child(2)::text').extract_first()
            item['area'] = float(i.css('p.house-about > span:nth-child(4)::text').re_first('[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0'))
            item['decoration'] = i.css('p.house-about.clearfix > span:nth-child(6)::text').extract_first()
            item['floor'] = i.css('p.house-about.clearfix > span:nth-child(8)::text').extract_first().strip()
            item['orientation'] = i.css('p.house-about.clearfix > span:nth-child(10)::text').extract_first().strip()
            item['build_year'] = int(i.css('p.house-about.clearfix > span:nth-child(12)::text').re_first(r'[1-9]\d*'))
            item['district'] = i.css('span.whole-line > a:nth-child(1)::text').extract_first()
            item['location'] = i.css('span.whole-line > a:nth-child(2)::text').extract_first()
            item['community'] = i.css('span.whole-line > a:nth-child(3)::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('?')[0]
            yield item

        le = LinkExtractor(restrict_css='.turnpage_next')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)
