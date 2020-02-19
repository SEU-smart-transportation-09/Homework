# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentkeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    course_name = scrapy.Field()
    course_organization = scrapy.Field()
    course_link = scrapy.Field()
    course_number = scrapy.Field()
    course_status = scrapy.Field()
    course_price = scrapy.Field()

    pass
