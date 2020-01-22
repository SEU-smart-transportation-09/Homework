# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class TencentclassesPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="stupid",
                                  db="homework",
                                  charset="utf8")
 
    def process_item(self, item, spider):
        title = item["title"]
        users = item["users"]
        price = item["price"]
        agency = item["agency"]
        cursor = self.conn.cursor()
        sql = "insert into TecentClasses(title, users_number, price, agency) values('%s', '%s', '%s', '%s');" % (title, users, price, agency)
        cursor.execute(sql)
        self.conn.commit()
        #print(title, users, price, agency)
        return item
 
    def close_spider(self,spider):
        self.conn.close()