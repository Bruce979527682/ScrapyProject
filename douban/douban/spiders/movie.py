# -*- coding: utf-8 -*-
import scrapy
import sys
import random
import sys
sys.path.append('./douban/')
from douban.utils import Utils

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    
    def start_requests(self):
        start_urls = ['http://movie.douban.com/']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('MovieSpider run')
        pass
