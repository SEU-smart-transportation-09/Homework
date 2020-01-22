# -*- coding: utf-8 -*-

# Author : JadeX
# Time   : 2020/1/21 21:11

import scrapy
import scrapytest_02.items


class Tc02Spider(scrapy.Spider):
    name = 'tc02'
    allowed_domains = ['ke.qq.com']
    url = 'https://ke.qq.com/course/list?page=%d'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    page_no = 1

    def start_requests(self):
        request = scrapy.Request(
            url=self.url % self.page_no,
            callback=self.extract_course,
            method='GET',
            headers=self.headers, errback=self.error_handle
        )
        return [request]

    def error_handle(self, err):
        print('错误')

    def extract_course(self, response):
        output = []
        courses = response.xpath('//div[@data-report-module="middle-course"]/ul/li')

        for course in courses:
            item_ = scrapytest_02.items.Scrapytest02Item()
            item_['name'] = course.xpath('h4/a/@title').get()
            item_['org'] = course.xpath('div/a/@title').get()
            item_['price'] = course.xpath('div/span[@class ="line-cell item-price  custom-string"]/text()').get()
            output.append(item_)

        if self.page_no <= 34:
            self.page_no += 1
            request = scrapy.Request(
                url=self.url % self.page_no,
                callback=self.extract_course,
                method='GET',
                headers=self.headers, dont_filter=True, errback=self.error_handle)
            output.append(request)

        return output