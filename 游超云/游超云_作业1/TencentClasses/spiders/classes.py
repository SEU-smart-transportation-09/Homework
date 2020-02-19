# -*- coding: utf-8 -*-
import scrapy
import re
from TencentClasses.items import TencentclassesItem
from scrapy.http import Request
from bs4 import BeautifulSoup



class ClassesSpider(scrapy.Spider):
    name = 'classes'
    # allowed_domains = ['ke.qq.com/']
    start_urls = ['https://ke.qq.com/course/list']
    
    def parse(self, response):
        item = TencentclassesItem()
        soup = BeautifulSoup(response.body, "html.parser")
        lis = soup.find_all('li', 'course-card-item--v3 js-course-card-item')
        divs = soup.find_all('div', 'item-line item-line--bottom')
        #print(soup.prettify())
        
        for li,div in zip(lis, divs):
            item['title'] = li.h4.a.attrs['title']
            #i.find('div', 'item-line item-line--middle').span.string
            item['users'] = re.search(r'[1-9]\d*.*人', div.find('span', 'line-cell item-user custom-string').string).group(0)
            item['price'] = div.find('span', 'line-cell item-price custom-string').string
            item['agency'] = li.find('div', 'item-line item-line--middle').a.attrs['title']
            yield item
 
        for i in range(2,416):
           nexturl = "https://ke.qq.com/course/list?page=" + str(i)
           yield Request(nexturl, callback = self.parse)
