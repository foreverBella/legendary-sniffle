# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import re
import numpy as np
import warnings
from pyecharts import Style, Geo, Map, Line, Pie



# 读取数据
df = pd.read_csv('D:\spider_project\douban\data.csv', names=['name', 'score', 'vote', 'date', 'href', 'comment'])

df.drop('href', axis=1, inplace=True)  # 去掉href列
df.drop_duplicates(subset=None, keep='first', inplace=True)  # 去重（这里没有重复值）
df.dropna(axis=0)  # 删除空值 (这里没有空值)
# 评分转换数字
df['score1'] = df['score']
df['score'] = df['score'].map({
    '力荐': 5,
    '推荐': 4,
    '还行': 3,
    '较差': 2,
    '很差': 1
})
warnings.filterwarnings('ignore')
df['date'] = pd.to_datetime(df['date']) # 将datetime字段由object转换成datetime类型，速度回快很多
df2 = df[df['score'] != '--'][['date', 'score', 'score1']]  # 去除未评分数据并取出date，score，score1三列
# 提取出5个评分的时间序列
df_5 = df2[df2['score'] == 5][['date', 'score1']]
df_4 = df2[df2['score'] == 4][['date', 'score1']]
df_3 = df2[df2['score'] == 3][['date', 'score1']]
df_2 = df2[df2['score'] == 2][['date', 'score1']]
df_1 = df2[df2['score'] == 1][['date', 'score1']]

# 统计每日评分次数
df_5 = df_5.groupby(['date']).count()
df_4 = df_4.groupby(['date']).count()
df_3 = df_3.groupby(['date']).count()
df_2 = df_2.groupby(['date']).count()
df_1 = df_1.groupby(['date']).count()

line = Line('评分趋势')
line.add('力荐', df_5.index.tolist(), df_5.score1.tolist())
line.add('推荐', df_4.index.tolist(), df_4.score1.tolist())
line.add('还行', df_3.index.tolist(), df_3.score1.tolist())
line.add('较差', df_2.index.tolist(), df_2.score1.tolist())
line.add('很差', df_1.index.tolist(), df_1.score1.tolist())

line

score_counts = df[df['score1'] != '--']['score1'].value_counts()
attr = score_counts.index.tolist()
value = score_counts[attr].tolist()

pie = Pie('各评分占比')
pie.add('', attr, value, radius=[30, 75], rosetype='radius', is_legend_show=False, is_label_show=True)
pie

'''
plt.figure(figsize=(16, 8))
plt.axis('off')#不显示坐标轴
plt.show()
'''