# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import AnjukeNewItem


class AnjukenewSpider(scrapy.Spider):
    name = 'anjukenew'
    allowed_domains = ['sz.fang.anjuke.com']
    start_urls = ['https://sz.fang.anjuke.com/loupan/']
    custom_settings = {
        'LOG_FILE': 'log_anjukenew.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.item-list.area-bd > div')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.item-list.area-bd > div.filter-sub')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_price)

    def parse_price(self, response):
        print('parse_price response.url:' + response.url)
        self.logger.debug('parse_price response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.filter-mod > div:nth-child(2) > div')
        print('3' * 80)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_hall)

    def parse_hall(self, response):
        print('parse_hall response.url:' + response.url)
        self.logger.debug('parse_hall response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.filter-mod > div:nth-child(3) > div')
        print('4' * 160)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = AnjukeNewItem()

        items = response.css('.key-list .item-mod')
        for i in items:
            item['title'] = i.css('.items-name::text').extract_first()
            item['url'] = i.css('.lp-name::attr(href)').extract_first()
            if i.css('.price-txt::text'):
                item['no_price'] = i.css('.price-txt::text').extract_first()
            if i.css('.price::text'):
                p = i.css('.price::text').extract()
                q = i.css('.price > span::text').extract()
                item['price'] = p[0].strip() + q[0] + p[1].strip()
            if i.css('.around-price::text'):
                p = i.css('.around-price::text').extract()
                q = i.css('.around-price > span::text').extract()
                item['price'] = p[0].strip() + q[0] + p[1].strip()
            item['phone'] = i.css('p.tel::text').extract_first()
            if i.css('.list-dp::text'):
                item['comment'] = int(i.css('.list-dp::text').re_first(r'[1-9]\d*|0'))
            item['img'] = i.css('img::attr(src)').extract_first()
            item['layout'] = '/'.join(i.css('a.huxing > span::text').extract()[0:-1])
            item['area'] = i.css('a.huxing > span::text').extract()[-1]
            comm_address = i.css('.list-map::text').extract_first().strip().split()
            item['district'] = comm_address[1]
            item['location'] = comm_address[2]
            item['address'] = comm_address[-1]
            item['status'] = i.css('i.status-icon.forsale::text').extract_first()
            item['type'] = i.css('i.status-icon.wuyetp::text').extract_first()
            getlocation(item)
            item['number'] = item['url'].split('/')[-1].split('.')[0]
            yield item

        le = LinkExtractor(restrict_css='a.next-page.next-link')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)
