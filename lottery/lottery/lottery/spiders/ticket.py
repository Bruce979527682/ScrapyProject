# -*- coding: utf-8 -*-
import scrapy


class TicketSpider(scrapy.Spider):
    name = 'ticket'
    allowed_domains = ['wx.zhcw.com']
    start_urls = ['http://wx.zhcw.com/']

    def parse(self, response):
        print('start')
