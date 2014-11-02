# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class ListExtractionPipeline(object):
    def process_item(self, item, spider):
        for key in item.keys():
            if (item[key]):
                if (type(item[key]) is list):
                    length = len(item[key])
                    if (length > 0):
                        if key not in item.__class__.LIST_KEYS:
                            item[key] = item[key][0]
                        spider.crawler.stats.inc_value(key + '_list_len_' + str(length))
                    else:
                        item[key] = None
                        spider.crawler.stats.inc_value(key + '_empty_list')
                else:
                    spider.crawler.stats.inc_value(key + '_not_list')
            else:
                item[key] = None
                spider.crawler.stats.inc_value(key + '_no_value')
        return item

class NamePipeline(object):
    def process_item(self, item, spider):
        if (item['name'] is None):
            raise DropItem("Missing name")
        return item

class SeenNamePipeline(object):
    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        if (item['name'] in self.name_seen):
            raise DropItem("Duplicate name %s" % item)
        self.name_seen.add(item['name'])
        return item
