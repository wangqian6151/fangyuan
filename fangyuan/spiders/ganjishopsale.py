# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import GanjiShopsaleItem


class GanjishopsaleSpider(scrapy.Spider):
    name = 'ganjishopsale'
    allowed_domains = ['sz.ganji.com']
    start_urls = ['http://sz.ganji.com/fang7/']

    custom_settings = {
        'LOG_FILE': 'log_ganjishopsale.txt',
    }

    def parse(self, response):
        print('parse response.url:' + response.url)
        self.logger.debug('parse response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.f-f-content > dl.fang5-area> dd > div > ul')
        print('1' * 20)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_region)

    def parse_region(self, response):
        print('parse_region response.url:' + response.url)
        self.logger.debug('parse_region response.url:' + response.url)
        yield Request(response.url, callback=self.parse_list)
        le = LinkExtractor(restrict_css='div.f-f-content > dl.fang5-area > dd > div > div')
        print('2' * 40)
        for link in le.extract_links(response):
            print(link, link.url, link.text)
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = GanjiShopsaleItem()

        div = response.css('div.f-list.js-tips-list > div.f-list-item')
        print('parse_list div:{}  response.url: {}'.format(div.css('dd.dd-item.title > a::text').extract(), response.url))
        self.logger.debug('parse_list div:{}  response.url: {}'.format(div.css('dd.dd-item.title > a::text').extract(), response.url))
        for i in div:
            item['title'] = i.css('dd.dd-item.title > a::text').extract_first()
            u = i.css('dd.dd-item.title > a::attr(href)').extract_first()
            if u.startswith('http'):
                item['url'] = u
                item['number'] = item['url'].split('?')[0].split('/')[-2]
            else:
                item['url'] = 'http://sz.ganji.com' + u
                item['number'] = item['url'].split('?')[0].split('/')[-1]
            if i.css('.unit::text').extract_first():
                item['total_price'] = i.css('.num::text').extract_first() + i.css('.unit::text').extract_first()
            else:
                item['total_price'] = i.css('.num::text').extract_first()
            item['uint_price'] = i.css('.small-price::text').extract_first()
            if i.css('img[data-original]'):
                item['img'] = i.css('img::attr(data-original)').extract_first()
            else:
                item['img'] = i.css('img::attr(src)').extract_first()
            con = i.css('dd.dd-item.size > span::text').extract()
            if len(con) == 3:
                item['area'] = float(re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0', con[0].strip())[0])
                item['floor'] = con[1].strip()
                item['type'] = con[2].strip()
            elif len(con) == 2:
                item['area'] = float(re.findall('[1-9]\d*\.\d*|0\.\d*[1-9]\d*|[1-9]\d*|0', con[0].strip())[0])
                item['floor'] = ''
                item['type'] = con[1].strip()
            else:
                item['area'] = 0
                item['floor'] = ''
                item['type'] = ''
            site = i.css('dd.dd-item.address > span.area > a::text').extract()
            if len(site) == 3:
                item['district'] = site[0].strip()
                item['location'] = site[1].strip().strip(' - ')
                item['address'] = site[2].strip().strip(' - ')
            elif len(site) == 2:
                item['district'] = site[0].strip()
                item['location'] = ''
                item['address'] = site[1].strip().strip(' - ')
            dd = i.css('dd.dd-item.feature > span::text').extract()
            item['tags'] = ' '.join(dd)
            # if len(dd) == 3:
            #     item['transfer'] = dd[0].strip()
            #     item['status'] = dd[1].strip().strip(' - ')
            #     item['industry'] = dd[2].strip().strip(' - ')
            # elif len(dd) == 2:
            #     item['transfer'] = dd[0].strip()
            #     item['status'] = dd[1].strip().strip(' - ')
            #     item['industry'] = ''

            # getlocation(item)
            # yield item
            self.logger.debug('parse_list item.url:' + item['url'])
            yield Request(url=item['url'], meta={'item': item}, callback=self.parse_details)

        le = LinkExtractor(restrict_css='ul.pageLink a.next')
        print('5' * 200)
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            print('next_url:', next_url)
            self.logger.debug('next_url:' + next_url)
            yield Request(next_url, callback=self.parse_list)

    def parse_details(self, response):
        item = response.meta['item']
        # item['payment'] = response.css(' ul.er-list.f-clear > li:nth-child(2) > span.content::text').extract_first()
        item['width'] = response.css(' ul.er-list.f-clear > li:nth-child(2) > span.content::text').extract_first()
        # item['lease'] = '/'.join(i.strip() for i in response.css('ul.er-list.f-clear > li:nth-child(4) > span.content::text').extract_first().split('/'))
        item['depth'] = response.css(' ul.er-list.f-clear > li:nth-child(3) > span.content::text').extract_first()
        item['sale'] = response.css(' ul.er-list.f-clear > li:nth-child(4) > span.content::text').extract_first().strip()
        item['height'] = response.css(' ul.er-list.f-clear > li:nth-child(5) > span.content::text').extract_first()
        if response.css(' ul.er-list.f-clear > li:nth-child(6) > span.content::text').extract_first():
            self.logger.debug('parse_details street:' + response.css(
                ' ul.er-list.f-clear > li:nth-child(6) > span.content::text').extract_first())
            item['street'] = response.css(' ul.er-list.f-clear > li:nth-child(6) > span.content::text').extract_first().strip(' - ')
        item['total_floor'] = response.css(' ul.er-list.f-clear > li:nth-child(7) > span.content::text').extract_first().strip()
        item['status'] = response.css(' ul.er-list.f-clear > li:nth-child(8) > span.content::text').extract_first().strip()
        if response.css('ul.er-list.f-clear > li:nth-child(10) > span.content a::text').extract_first():
            self.logger.debug('parse_details industry:' + response.css('ul.er-list.f-clear > li:nth-child(10) > span.content::text').extract_first())
            item['industry'] = response.css('ul.er-list.f-clear > li:nth-child(10) > span.content a::text').extract_first()
        else:
            item['industry'] = response.css('ul.er-list.f-clear > li:nth-child(10) > span.content::text').extract_first().strip()

        # 获取经纬度方法一
        lnglat = re.findall(r'coord=(.*);">', response.text)[0].split(',')
        item['lng'] = float(lnglat[0])
        item['lat'] = float(lnglat[1])
        # #获取经纬度方法二
        # lnglat = json.loads(response.css('#baidu_Map::attr(data-ref)').extract_first()).get('lnglat').strip('b').split(',')
        # item['lng'] = float(lnglat[0])
        # item['lat'] = float(lnglat[1])
        return item

