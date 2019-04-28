# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Tencent.items import ContentItem, TencentItem


class TencentSpider(CrawlSpider):
    name = "tencent"
    allowed_domains = ["tencent.com"]
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']
    base_url = 'https://hr.tencent.com/'
    rules = (Rule(
        LinkExtractor(allow=r'start=\d+'), callback='parse_item',
        follow=True), )

    def parse_item(self, response):

        node_list = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath(
                './td[1]/a/text()').extract_first()
            item['position_link'] = node.xpath(
                './td[1]/a/@href').extract_first()
            item['position_type'] = node.xpath(
                './td[2]/text()').extract_first()
            item['people_number'] = node.xpath(
                './td[3]/text()').extract_first()
            item['work_location'] = node.xpath(
                './td[4]/text()').extract_first()
            item['publish_times'] = node.xpath(
                './td[5]/text()').extract_first()

            yield item

            if item['position_link']:
                yield scrapy.Request(
                    self.base_url + item['position_link'],
                    callback=self.parse_content)

    def parse_content(self, response):
        item = ContentItem()
        nodes = response.xpath('//ul[@class="squareli"]')

        item['position_link'] = response.url
        item['position_content'] = nodes[0].xpath('.//text()').extract()
        item['position_request'] = nodes[-1].xpath('.//text()').extract()
        yield item
