# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import AnjukeShopsaleItem


class AnjukeshopsaleSpider(scrapy.Spider):
    name = 'anjukeshopsale'
    allowed_domains = ['sz.sp.anjuke.com']
    start_urls = ['https://sz.sp.anjuke.com/shou/']

    custom_settings = {
        'LOG_FILE': 'log_anjukeshopsale.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-mod > div:nth-child(1) > div.elems-l')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='.items-mod > div:nth-child(1) > div > div.sub-items')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = AnjukeShopsaleItem()

        li = response.css('#list-content>.list-item')
        for i in li:
            item['title'] = i.css('.item-title::text').extract_first().strip()
            item['url'] = i.xpath('@link').extract_first()
            item['total_price'] = i.css('em::text').extract_first() + i.css('.price-a::text').extract()[1].strip()
            item['unit_price'] = i.css('.price-b::text').extract_first().strip()
            item['img'] = i.css('img::attr(src)').extract_first()
            item['area'] = int(i.css('dl > dd:nth-child(2) > span:nth-child(1)::text').re_first('[1-9]\d*|0'))
            item['floor'] = i.css('dl > dd:nth-child(2) > span:nth-child(3)::text').extract_first()
            item['type'] = i.css('dl > dd:nth-child(2) > span:nth-child(5)::text').extract_first()
            item['community'] = i.css('dd.address > a::text').extract_first()
            # comm_address = i.css('dd.address > span::text').extract_first().split()
            # print("i.css('dd.address > span::text'):" + i.css('dd.address > span::text').extract_first())
            # self.logger.debug("i.css('dd.address > span::text'):" + i.css('dd.address > span::text').extract_first())
            if i.css('dd.address > span::text').extract_first():
                comm_address = i.css('dd.address > span::text').extract_first().split()
                print('parse_list comm_address:' + str(comm_address))
                self.logger.debug('parse_list comm_address:' + str(comm_address))
                total_adress = comm_address[0].strip('[').split('-')
                item['district'] = total_adress[0]
                item['location'] = total_adress[1]
                if len(comm_address) > 1:
                    item['address'] = comm_address[1].strip(']')
                else:
                    item['address'] = ''
            else:
                item['district'] = ''
                item['location'] = ''
                item['address'] = ''
            getlocation(item)
            item['number'] = item['url'].split('?', 1)[0].split('/')[-2]
            yield item

        le = LinkExtractor(restrict_css='div.multi-page > a.aNxt')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)

