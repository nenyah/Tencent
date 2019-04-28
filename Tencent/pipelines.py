# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from Tencent.items import ContentItem, TencentItem


class TencentPipeline(object):
    def __init__(self):
        self.itemfile = open('tencent.json', 'w')
        self.contentfile = open('tencent_cotent.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, TencentItem):
            content = json.dumps(
                dict(item), ensure_ascii=False, indent=4) + ",\n"
            self.itemfile.write(content)
        elif isinstance(item, ContentItem):
            content = json.dumps(
                dict(item), ensure_ascii=False, indent=4) + ",\n"
            self.contentfile.write(content)
        return item

    def close_spider(self, spider):
        self.itemfile.close()
        self.contentfile.close()
