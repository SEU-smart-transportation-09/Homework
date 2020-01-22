# -*- coding: utf-8 -*-

# Author : JadeX
# Time   : 2020/1/21 20:50

import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt

# 爬虫
def get_data(url):

    resp = requests.get(url)
    html = resp.content.decode('gbk')
    soup = BeautifulSoup(html, 'html.parser')
    tr_list = soup.find_all('tr')
    dates, conditions, temp = [], [], []
    for data in tr_list[1:]:
        sub_data = data.text.split()
        dates.append(sub_data[0])
        conditions.append(''.join(sub_data[1:3]))
        temp.append(''.join(sub_data[3:6]))
    _data = pd.DataFrame()
    _data['日期'] = dates
    _data['天气状况'] = conditions
    _data['气温'] = temp
    return _data

data_1 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201901.html')
data_2 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201902.html')
data_3 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201903.html')
data_4 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201904.html')
data_5 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201905.html')
data_6 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201906.html')
data_7 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201907.html')
data_8 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201908.html')
data_9 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201909.html')
data_10 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201910.html')
data_11 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201911.html')
data_12 = get_data('http://www.tianqihoubao.com/lishi/suzhou/month/201912.html')


data = pd.concat([data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9, data_10, data_11, data_12]).reset_index(drop=True)

data.to_csv('szweather2019_02.csv', index=False, encoding='utf-8')

# 数据可视化

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
data2 = pd.read_csv('szweather2019_02.csv')

data2['最高气温'] = data2['气温'].str.split('/', expand=True)[0]
data2['最低气温'] = data2['气温'].str.split('/', expand=True)[1]
data2['最高气温'] = data2['最高气温'].map(lambda x: int(x.replace('℃', '')))
data2['最低气温'] = data2['最低气温'].map(lambda x: int(x.replace('℃', '')))

date = data2['日期']
high = data2['最高气温']
low = data2['最低气温']

fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(date, high, c='red', alpha=0.5)
plt.plot(date, low, c='blue', alpha=0.5)
plt.fill_between(date, high, low, facecolor='blue', alpha=0.2)

plt.title('苏州2019年气温折线图', fontsize=18)
plt.xlabel('', fontsize=5)
fig.autofmt_xdate()
plt.ylabel('气温', fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=10)
plt.xticks(date[::20])

plt.show()



