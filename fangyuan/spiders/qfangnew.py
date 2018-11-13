# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from fangyuan.html_from_url import getlocation
from fangyuan.items import QfangNewItem


class QfangnewSpider(scrapy.Spider):
    name = 'qfangnew'
    allowed_domains = ['shenzhen.qfang.com']
    start_urls = ['https://shenzhen.qfang.com/newhouse/list']

    custom_settings = {
        'LOG_FILE': 'log_qfangnew.txt',
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
            yield Request(link.url, callback=self.parse_list)

    def parse_list(self, response):
        print('parse_list response.url:' + response.url)
        self.logger.debug('parse_list response.url:' + response.url)

        item = QfangNewItem()

        items = response.css('#newhouse-list > .clearfix')
        for i in items:
            item['title'] = i.css('.house-title a::text').extract_first().strip()
            # if i.css('.alias-text::text'):
                # item['alias'] = i.css('.alias-text::text').extract_first()
            item['alias'] = i.css('div.house-title.clearfix > span::text').extract_first()
            item['url'] = 'https://shenzhen.qfang.com' + i.css('.house-title a::attr(href)').extract_first()
            item['status'] = i.css('.state-label::text').extract_first()
            # item['status'] = i.css('div.house-title.clearfix > span::text').extract_first()
            item['unit_price'] = i.css('.sale-price::text').extract_first()
            if i.css('.show-price p::text'):
                item['total_price'] = i.css('.show-price p::text').extract_first()
            item['img'] = i.css('img::attr(src)').extract_first().strip()
            desc = i.css('div.natures > span::text').extract()
            if len(desc) == 3:
                item['district'] = desc[0].split()[0]
                item['location'] = desc[0].split()[1]
                item['type'] = ' '.join(desc[1].strip().split())
                item['decoration'] = desc[2].strip()
            elif len(desc) == 2:
                item['district'] = desc[0].split()[0]
                item['location'] = desc[0].split()[1]
                item['decoration'] = desc[1].strip()
            # item['district'] = i.css('div.natures > span:nth-child(1)::text').extract_first().split()[0]
            # item['location'] = i.css('div.natures > span:nth-child(1)::text').extract_first().split()[1]
            # item['type'] = i.css('div.natures > span:nth-child(3)::text').extract_first().strip()
            # item['decoration'] = i.css('div.natures > span:nth-child(5)::text').extract_first().strip()
            item['layout'] = ' '.join(i.css('div.new-house-dsp > p:nth-child(1) > span::text').extract())
            item['area'] = i.css('div.new-house-dsp > p:nth-child(2) > span::text').extract_first()
            item['time'] = i.css('div.new-house-dsp > p:nth-child(3) > span::text').extract_first().strip()
            item['address'] = i.css('div.new-house-dsp > p:nth-child(4) > span::text').extract_first().strip()
            if i.css('p.new-house-phone > em'):
                phone_list = i.css('p.new-house-phone::text').extract()
                phone_text = i.css('p.new-house-phone > em::text').extract_first()
                item['phone'] = phone_list[0].strip() + phone_text + phone_list[1].strip()
            else:
                item['phone'] = i.css('p.new-house-phone::text').extract_first()
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
