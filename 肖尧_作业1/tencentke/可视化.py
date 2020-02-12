# 将爬下来的课程信息根据报名人数和课程价格计算出赚钱最多的教育机构

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

course = pd.read_csv('course.csv')

# 数据清洗，把csv文件中多余的文字删除，只留数字部分， 同时增加一行‘利润’
def revenue_cal(datframe):
    out = {}
    try:
        course_price = float(datframe['course_price'][1:])
        course_number = float(datframe['course_number'][:-3])
        out['revenue'] = course_price * course_number
    except:
        pass

    return pd.Series(out)


figure = plt.figure(figsize=(10, 4)) # 画布大小
course['revenue'] = course.apply(revenue_cal, axis=1)
sorted_course = course.sort_values(by=['revenue'], ascending=False).head(10)
plt.tick_params(axis='x', labelsize=10)
plt.rcParams['font.sans-serif'] = ['SimHei']
bar = plt.bar(sorted_course['course_organization'], sorted_course['revenue'].values)
for a, b in zip(sorted_course['course_organization'], sorted_course['revenue']):
    plt.text(a, b + 0.1, '%.2f' % (b / 10000000), ha='center', va='bottom')

plt.title(u'腾讯课堂最赚钱的课程与教学机构排名')
plt.xlabel('机构名')
plt.ylabel(u'利润金额(百万)')
plt.show()
figure.savefig('a.png')