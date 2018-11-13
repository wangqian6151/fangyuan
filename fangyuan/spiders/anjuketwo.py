# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import AnjukeTwoItem


class AnjuketwoSpider(scrapy.Spider):
    name = 'anjuketwo'
    allowed_domains = ['shenzhen.anjuke.com']
    start_urls = ['https://shenzhen.anjuke.com/sale/']
    custom_settings = {
        'LOG_FILE': 'log_anjuketwo.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-list > div:nth-child(1) > span.elems-l')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-list > div:nth-child(1) > span.elems-l > div')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_area)

    def parse_area(self, response):
        print('parse_area response.url:' + response.url)
        self.logger.debug('parse_area response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-list > div:nth-child(3) > span.elems-l')
        print('3' * 80)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_hall)

    def parse_hall(self, response):
        print('parse_hall response.url:' + response.url)
        self.logger.debug('parse_hall response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-list > div:nth-child(4) > span.elems-l')
        print('4' * 160)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = AnjukeTwoItem()

        li = response.css('.houselist-mod-new>li')
        for i in li:
            item['title'] = i.css('.house-title a::text').extract_first().strip()
            item['url'] = i.css('.house-title a::attr(href)').extract_first().split('?', 1)[0]
            item['total_price'] = float(i.css('strong::text').extract_first())
            item['unit_price'] = int(i.css('.unit-price::text').re_first(r'[1-9]\d*|0'))
            item['img'] = i.css('img::attr(src)').extract_first()
            item['layout'] = i.css('div.house-details > div:nth-child(2) > span:nth-child(1)::text').extract_first()
            item['area'] = i.css('div.house-details > div:nth-child(2) > span:nth-child(3)::text').extract_first()
            item['floor'] = i.css('div.house-details > div:nth-child(2) > span:nth-child(5)::text').extract_first()
            item['build_year'] = i.css('div.house-details > div:nth-child(2) > span:nth-child(7)::text').extract_first()
            if i.css('.comm-address::text').extract_first():
                comm_address = i.css('.comm-address::text').extract_first().strip().split()
                print('comm_address :', comm_address)
                self.logger.debug('comm_address :' + str(comm_address))
                item['community'] = comm_address[0]
                total_adress = comm_address[1].split('-')
                # print('total_adress :', total_adress)
                item['district'] = total_adress[0]
                item['location'] = total_adress[1]
                item['address'] = total_adress[2]
                getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('?')[0]
            yield item

        le = LinkExtractor(restrict_css='div.multi-page > a.aNxt')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)

