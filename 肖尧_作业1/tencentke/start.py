from scrapy import cmdline

cmdline.execute("scrapy crawl course -o course.csv".split())