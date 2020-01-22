import pandas as pd
from matplotlib import pyplot as plt

# Author : JadeX
# Time   : 2020/1/21 21:33

plt.rcParams['font.sans-serif'] = ['SimHei']
data = pd.read_csv('tctest_02.csv')

price_free = 0
price_onedigit = 0
price_doubledigit = 0
price_threedigit = 0
price_fourdigit = 0
price_fivedigit = 0

for prices in data['price']:
    if prices == '免费' or '':
        price_free += 1
    else:
        if type(prices) == str:
            price_num = float(prices[1:])
        else:
            price_num = prices
        # 这里报错了很多次……因为提取到的价格的数值类型有str和float两种 所以处理方式也不一样

        if 0 < price_num < 10:
            price_onedigit += 1
        elif 10 <= price_num < 100:
            price_doubledigit += 1
        elif 100 <= price_num < 1000:
            price_threedigit += 1
        elif 1000 <= price_num < 10000:
            price_fourdigit += 1
        elif 10000 <= price_num:
            price_fivedigit += 1

print(price_free, price_onedigit, price_doubledigit, price_threedigit, price_fourdigit, price_fivedigit)

course_price = ['免费', '一位数', '二位数', '三位数', '四位数', '五位数']
course_counts = [price_free, price_onedigit, price_doubledigit, price_threedigit, price_fourdigit, price_fivedigit]

plt.pie(course_counts,
        labels=course_price,
        startangle=0,
        explode=(0.1, 0, 0, 0, 0, 0.2)
        # , autopct='%1.0f%%'
        )
plt.title('腾讯课堂课程价格分布饼图')
plt.show()







