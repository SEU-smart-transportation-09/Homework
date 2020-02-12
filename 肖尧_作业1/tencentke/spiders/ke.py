from scrapy import Request
from scrapy.spiders import Spider
from tencentke.items import TencentkeItem
import scrapy


# class CourseSpider(scrapy.Spider):
#     name = 'course'
#     allowed_domains = ['ke.qq.com']
#     start_urls = ['https://ke.qq.com/course/list?mt=1001&st=2002&tt=3019&price_min=1&page=1']
#
#     def parse(self, response):
#         result = response.xpath('//section[1]/div/div[3]/ul/li')
#         items = []  # 数据项数组列表
#         for course_ in result:
#             # 数据项
#             item_ = TencentkeItem()
#             course_name = course_.xpath('h4/a/text()').get()
#             item_['course_name'] = '{}'.format(course_name.strip() if course_name else '')
#             # 培训机构
#             course_organization = course_.xpath(
#                 'div[@class="item-line item-line--middle"]/a[@rel="nofollow"]/text()').get()
#             item_['course_organization'] = course_organization.strip() if course_organization else ''
#             # 课程连接
#             course_link = course_.xpath('a/@href').get()
#             item_['course_link'] = course_link.strip() if course_link else ''
#             # 报名人数
#             course_number = course_.xpath(
#                 'div[2]/span[@class="line-cell item-user custom-string"]/text()').get()
#             item_['course_number'] = course_number.strip() if course_number else ''
#             # 课程状态
#             course_status = course_.xpath('div[@class="item-line item-line--middle"]/span[@class="line-cell '
#                                           'item-task"]/text()').get()
#             item_['course_status'] = course_status.strip() if course_status else ''
#             # 课程价格
#             course_price = course_.xpath('div[2]/span[1]/text()').get()
#             item_['course_price'] = course_price.strip() if course_price else ''
#             items.append(item_)
#         # 返回数据项到管道
#         return items

class CourseSpider(Spider):
    name = 'course'
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.100 Safari/537.36'}
    allowed_domains = ['ke.qq.com']
    current_page = 1

    def start_requests(self):
        url = 'https://ke.qq.com/course/list?mt=1001&st=2002&tt=3019&price_min=1&page=1'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        result = response.xpath('//section[1]/div/div[3]/ul/li')
        item_ = TencentkeItem()
        for course_ in result:
            # 数据项
            course_name = course_.xpath('h4/a/text()').get()
            item_['course_name'] = '{}'.format(course_name.strip() if course_name else '')
            # 培训机构
            course_organization = course_.xpath(
                'div[@class="item-line item-line--middle"]/a[@rel="nofollow"]/text()').get()
            item_['course_organization'] = course_organization.strip() if course_organization else ''
            # 课程连接
            course_link = course_.xpath('a/@href').get()
            item_['course_link'] = course_link.strip() if course_link else ''
            # 报名人数
            course_number = course_.xpath(
                'div[2]/span[@class="line-cell item-user custom-string"]/text()').get()
            item_['course_number'] = course_number.strip() if course_number else ''
            # 课程状态
            course_status = course_.xpath('div[@class="item-line item-line--middle"]/span[@class="line-cell '
                                          'item-task"]/text()').get()
            item_['course_status'] = course_status.strip() if course_status else ''
            # 课程价格
            course_price = course_.xpath('div[2]/span[1]/text()').get()
            item_['course_price'] = course_price.strip() if course_price else ''
            yield item_
        # 返回数据项到管道

        self.current_page += 1
        url_next = 'https://ke.qq.com/course/list?mt=1001&st=2002&tt=3019&price_min=1&page=' + str(self.current_page)
        # total_page = response.xpath('/html/body/section[1]/div/div[5]/a[5]/text()').extract_first()
        if self.current_page <= 21:
            yield Request(url_next, headers=self.headers)
