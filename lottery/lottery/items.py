# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LotteryItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    
class TicketItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    num = scrapy.Field()
    blue = scrapy.Field()
    red = scrapy.Field()
    remark = scrapy.Field()
