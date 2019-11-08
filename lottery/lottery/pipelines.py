# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class LotteryPipeline(object):
    def process_item(self, item, spider):
        return item
 
class TicketItemPipeline(object):    
    def process_item(self, item, spider):
        if item.get('date'):
            return item
        else:
            raise DropItem("Missing date in %s" % item)    
    
class MongoPipeline(object):    
    collection_name = 'Scrapy'    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        dblist = self.client.list_database_names()
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.get('date'):            
            self.db[self.collection_name].insert_one(dict(item))
            return item
        else:
            raise DropItem("Missing date in %s" % item)
