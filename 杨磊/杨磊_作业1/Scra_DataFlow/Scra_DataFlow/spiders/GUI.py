
#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt
import pandas as pd
import numpy as np

alg = pd.read_csv('D:\文档\python程序\enke\Scra_DataFlow\course.csv', usecols=['course_name', 'course_organization'])

gr = alg.groupby(['course_organization'])

df = gr.count()
print(df)
df.plot()

# fig = plt.figure()                      # 创建一个没有 axes 的 figure
# fig.suptitle('No axes on this figure')  # 添加标题以便我们辨别
#
# fig, ax_lst = plt.subplots(2, 2)        # 创建一个以 axes 为单位的 2x2 网格的 figure
plt.show()

