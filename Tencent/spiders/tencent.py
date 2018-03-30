# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["tencent.com"]
    base_url = "https://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract()[0]

            item['position_link'] = node.xpath("./td[1]/a/@href").extract()[0]

            if len(node.xpath("./td[2]/text()")):
                item['position_type'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['position_type'] = ""

            item['people_number'] = node.xpath("./td[3]/text()").extract()[0]

            item['work_location'] = node.xpath("./td[4]/text()").extract()[0]

            item['pub_date'] = node.xpath("./td[5]/text()").extract()[0]

            yield item
            
        if not len(response.xpath('//a[@class="noactive" and @id="next"]')):
            next_page_url = response.xpath('//a[@id="next"]/@href').extract()[0]
            url = "https://hr.tencent.com/" + next_page_url
            yield scrapy.Request(url, callback=self.parse)
        # if self.offset < 2190:
        #     self.offset += 10
        #     url = self.base_url + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)