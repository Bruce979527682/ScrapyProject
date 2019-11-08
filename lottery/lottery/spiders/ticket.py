# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from lottery.items import TicketItem

class TicketSpider(scrapy.Spider):
    name = 'ticket'
    allowed_domains = ['kaijiang.zhcw.com']
    #start_urls = ['http://wx.zhcw.com/h5/port/client_json.php?lottery=FC_SSQ&pageSize=100&pageNo=1&transactionType=300301&src=0000100001%7C6000003060']

    def start_requests(self):
        urls = [
            'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
        ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_bs)
            
    def parse(self, response):# 使用Scrapy内置解析
        title = response.css('title::text').get() # title2 = response.xpath('//title/text()').get()         
        trs = response.css('table tr').getall()
        for index,item in enumerate(trs):
            if index > 1:
                try:                
                    td = Selector(text=item)                
                    reds = [td.css('em::text')[0].get(),td.css('em::text')[1].get(),td.css('em::text')[2].get(),td.css('em::text')[3].get(),td.css('em::text')[4].get(),td.css('em::text')[5].get()]             
                    blue = td.css('em::text')[6].get() # blue = td.xpath('//td/em[7]/text()').get()   
                    yield TicketItem({'date': td.css('td::text')[0].get(), 'num': td.css('td::text')[1].get(), 'red': ' '.join(reds), 'blue': blue})
                except Exception as err:
                    print('此页最后一条：' + str(index))
        try:            
            next_page = response.css('p.pg a::attr(href)')[2].get() # next_page = response.css('p.pg a::attr(href)')[2].extract()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except Exception as ex:
            print('获取下一页异常：' + ex)
            
    def parse_bs(self, response):# 使用BeautifulSoup解析
        soup = BeautifulSoup(response.body, 'html.parser')
        trs = soup.find_all('tr')
        for index,item in enumerate(trs):
            if index > 1:
                try:                
                    tds = item.find_all('td')                
                    ems = tds[2].contents                
                    reds = [ems[1].next,ems[3].next,ems[5].next,ems[7].next,ems[9].next,ems[11].next]             
                    blue = ems[13].next
                    yield TicketItem({'date': tds[0].next, 'num': tds[1].next, 'red': ' '.join(reds), 'blue': blue})
                except Exception as err:
                    print('此页最后一条：' + str(index))
        try:
            next_page = soup.select('p.pg a')[2].get('href')
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_bs)
        except Exception as ex:
            print('获取下一页异常：' + ex)            
        
