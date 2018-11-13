# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import TongchengShopsaleItem


class TongchengshopsaleSpider(scrapy.Spider):
    name = 'tongchengshopsale'
    allowed_domains = ['sz.58.com']
    start_urls = ['http://sz.58.com/shangpucs/']

    custom_settings = {
        'LOG_FILE': 'log_tongchengshopsale.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.filter-wrap > dl:nth-child(1) > dd')
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
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = TongchengShopsaleItem()

        li = response.css('.house-list-wrap>li')
        for i in li:
            self.logger.debug('11111111111parse_list response.url:' + response.url)
            item['title'] = i.css('.title_des::text').extract_first().strip()
            item['number'] = i.xpath('@logr').extract_first().split('_')[3]
            item['url'] = 'https://sz.58.com/shangpu/' + item['number'] + 'x.shtml'
            item['total_price'] = i.css('p.sum > b::text').extract_first()
            item['unit_price'] = i.css('.unit span::text').extract_first()
            # item['time'] = i.css('.time::text').extract_first()
            item['img'] = i.css('img::attr(data-src)').extract_first()
            # print('area : {}'.format(i.css('div.list-info > p:nth-child(2) > span:nth-child(1)::text').re_first('\d+(\.\d+)?')))
            # self.logger.debug('area : {}'.format(i.css('div.list-info > p:nth-child(2) > span:nth-child(1)::text').re_first('\d+(\.\d+)?')))
            # item['area'] = float(
            #     i.css('div.list-info > p:nth-child(2) > span:nth-child(1)::text').re_first(r'\d+(\.\d+)?'))
            con = i.css('div.list-info > p:nth-child(2) > span::text').extract()
            if len(con) == 3:
                item['area'] = con[0].strip()
                item['type'] = con[1].strip()
                item['status'] = con[2].strip()
            elif len(con) == 2:
                item['area'] = con[0].strip()
                item['status'] = con[1].strip()
            # item['area'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(1)::text').extract_first()
            # item['type'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(2)::text').extract_first()
            # item['status'] = i.css('div.list-info > p:nth-child(2) > span:nth-child(3)::text').extract_first()
            loc = i.css('div.list-info > p:nth-child(3) > span:nth-child(1)::text').extract_first().split('-')
            self.logger.debug('2222222222222parse_list loc:' + str(loc))
            item['district'] = loc[0].strip()
            if len(loc) > 1:
                item['location'] = loc[1].strip()
            else:
                item['district'] = ''

            if i.css('div.list-info > p:nth-child(3) > span:nth-child(2)::text'):
                item['address'] = i.css(
                    'div.list-info > p:nth-child(3) > span:nth-child(2)::text').extract_first().replace(
                    '-', '')
            else:
                item['address'] = ''
            item['tags'] = ' '.join(i.css('div.list-info > p.tag-wrap > span::text').extract())
            getlocation(item)
            yield item

        le = LinkExtractor(restrict_css='div.pager > a.next')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)
