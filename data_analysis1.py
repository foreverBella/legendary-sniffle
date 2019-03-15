import re  # 正则表达式库
import numpy as np
import codecs
import collections  # 词频统计库
import wordcloud  # 词云展示库
from PIL import Image  # 图像处理库
import matplotlib.pyplot as plt
import jieba
from snownlp import SnowNLP



string_data = codecs.open('data.txt', 'r', encoding='utf-8').read()

# 文本预处理
pattern = re.compile(u'\t|\r|\n|\.|-|:|;|\)|\,|\，|\；|\：|\…|\"|\(|\?|\《|\》|\”|\|"')  # 定义正则表达式匹配模式
string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

# 文本分词
seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
object_list = []
remove_words = [u'的', u'，', u'和', u'是', u'随着', u'着',u'对于', u'对', u'等', u'能', u'都', u'。',u'还是',u'‘', u' ', u'、', u'！',u'一个',u'？',u'‘',u'“',u'‘',u'...',u'（',u'）',u'中',u'与',
    u'给', u'到',u'在',  u'大',u'人类',u'但是',u'得',u'真的',u'了', u'但',u'不',u'有',u'上', u'人', u'很',u'看',u'说',u'还',u'没有',u'这',u'让',u'通常', u'不是',u'如果', u'我', u'需要',u'也',u'电影','就']  # 自定义去除词库

for word in seg_list_exact:  # 循环读出每个分词
    if word not in remove_words:  # 如果不在去除词库中
        object_list.append(word)  # 分词追加到列表

# 词频统计
word_counts = collections.Counter(object_list)  # 对分词做词频统计
word_counts_top10 = word_counts.most_common(10)  # 获取前10最高频的词
print(word_counts_top10)  # 输出检查




# 词频展示
mask= np.array(Image.open('c.png'))  # 定义词频背景
wc = wordcloud.WordCloud(
       font_path='C:\Windows\Fonts\simsun.ttc',  # 指定中文字体
        background_color='red',  # 设置背景颜色
        max_words=2000,  # 设置最大显示的字数
        mask=mask,  # 设置背景图片
        max_font_size=200,  # 设置字体最大值
        random_state=20  # 
)
wc.generate_from_frequencies(word_counts)# 从字典生成词云
wc.to_file('results.jpg')
image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
#wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
plt.imshow(wc)  # 显示词云
plt.axis('off')  # 关闭坐标轴
plt.show()  # 显示图像



f = open('data1.csv', 'r', encoding='UTF-8')
list = f.readlines()
sentimentslist = []
for i in list:
    s = SnowNLP(i)
    #print(i)
    #print(s.sentiments)
    sentimentslist.append(s.sentiments)

plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='g')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.show()

def get_pos_neg_all(list):
    pos_text=''
    neg_text=''
    comment_text=''
    with open('pos.txt', 'w', encoding='utf-8') as pos, open('neg.txt', 'w', encoding='utf-8') as neg,open('comment.txt', 'w', encoding='utf-8') as comment:
        for i in list:

            comment.write(i)
            s=i.strip()
            comment_text+=s


            try:
                if SnowNLP(s).sentiments>0.5:
                    pos_text+=s
                    pos.write(s)

                else:
                    neg_text+=s
                    neg.write(s)
            except:
                continue
    return pos_text,neg_text,comment_text

pos_text,neg_text,comment_text=get_pos_neg_all(list)
