# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from tencentke.TencentNumTrans import TencentKedict
from tencentke.items import TencentkeItem


class TencentkePipeline(object):
    def process_item(self, item, spider):
        newitem = TencentkeItem()
        # 处理course_name
        newitem['course_name'] = item['course_name']
        # 处理course_organization
        newitem['course_organization'] = item['course_organization']
        # 处理course_link
        newitem['course_link'] = item['course_link']
        # 处理course_status
        newitem['course_status'] = item['course_status']
        # 处理course_price 原HTML文件中的数字与实际数字不一致，处理之
        if item['course_price']:
            templist = []
            for i in item['course_price']:
                if i in TencentKedict:
                    templist.append(TencentKedict[i])
                else:
                    templist.append(i)
            newitem['course_price'] = ''.join(templist)
        # 处理course_number 原HTML文件中的数字与实际数字不一致，处理之
        if item['course_number']:
            templist = []
            for i in item['course_number']:
                if i in TencentKedict:
                    templist.append(TencentKedict[i])
                else:
                    templist.append(i)
            newitem['course_number'] = ''.join(templist)

        return newitem
