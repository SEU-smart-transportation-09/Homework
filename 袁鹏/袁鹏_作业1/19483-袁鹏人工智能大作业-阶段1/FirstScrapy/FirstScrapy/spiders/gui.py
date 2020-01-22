# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# alg = pd.read_csv('C:\\Users\\yuanpeng\\FirstScrapy\\Scra_DataFlow\\course.csv', usecols=['course_name', 'course_organization'])
#
# gr = alg.groupby(['course_organization'])
#
# df = gr.count()
#
# # 使用索引添加一列
# df['course_organization'] = df.index
# # 添加一列数值
# df['百分比'] = [50, 40,80,60, 10, 20, 70, 30,50, 40,80,60, 10, 20, 70, 30]
# print(df.index.values)
# ax = df.plot(xticks=[0,1,2,3,4,5,6,7] ,yticks=[10,20,30,40,50,60,70,80,90] ,figsize=(12,4), legend=False)   # 不使用索引作为坐标轴。自动生成x坐标轴。
#
# ax.set_xlabel('培训机构', labelpad=10)
# ax.set_xlim(0,17)
# ax.set_ylim(0,90)


#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
import matplotlib.pyplot as plt   # 导入模块 matplotlib.pyplot，并简写成 plt
import pandas as pd
import numpy as np

alg = pd.read_csv('C:\\Users\\yuanpeng\\FirstScrapy\\FirstScrapy\\course.csv', usecols=['course_name', 'course_organization'])

gr = alg.groupby(['course_organization'])

df = gr.count()
print(df)
df.plot()

# fig = plt.figure()                      # 创建一个没有 axes 的 figure
# fig.suptitle('No axes on this figure')  # 添加标题以便我们辨别
#
# fig, ax_lst = plt.subplots(2, 2)        # 创建一个以 axes 为单位的 2x2 网格的 figure
plt.show()