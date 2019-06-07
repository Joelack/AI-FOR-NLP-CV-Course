
# import pandas as pa
# dataframe=pa.read_csv('sqlResult_1558435.csv',encoding='gb18030')
# #print(dataframe.head())
# all_articles=dataframe['content'].tolist();
# print(all_articles[:5])
import os
import re
import jieba
from collections import Counter
import pandas as pa
def get_text():
    # pattern='wiki.zh_\d.txt'
    # filename=re.findall(pattern,''.join(os.listdir()))
    # text=""
    # for name in filename:
    #     file=open(name,encoding="UTF-8")
    #     text+=file.read()
    # print("get_text()")
    text=pa.read_csv('sqlResult_1558435.csv',encoding='gb18030')
    text=text['content'].tolist()
    text=''.join([ str(i) for i in text])
    print('get_text() down',text[:1000])
    return text
def clean_text(text):
    #删除字符
    pattern="[\w|\d]+"
    text=''.join(re.findall(pattern,text))
    text=text.replace(' ', '').replace('n', '')
    print('clean_text() down', text[:1000])
    return text

def cut_text(text):
    text=list(jieba.cut(text))
    print('cut_text() down', text[:1000])
    return text
def count_text(text):
    text=Counter(text)
    #print('cut_text() down',text.most_common(10))
    return  text
def get_prob(word,text,Max):
    if word not in text:return 1/Max
    return text[word]/Max
def lang_mode(sentence,text,text_2,Max,Max2,mode=1):
    words=cut_text(sentence)
    pro=1
    if mode==1:#1-gram
        for i in words:
            pro*=get_prob(i,text,Max)

    else:#2-gram
        for i,j in enumerate(words):
            if i==0:
                pro*=get_prob(j,text,Max)
            else:
                pro*=get_prob(words[i-1]+words[i],text_2,Max2)/get_prob(words[i-1],text,Max)
    return pro

def main():
    text=cut_text(clean_text(get_text()))
    textcount=len(text)
    text_2 = [text[i]+text[i+1] for i,j in enumerate(text) if i!=textcount-1]
    textcount_2=len(text_2)
    text = count_text(text)
    text_2 = count_text(text_2)
    print("总共包含{}个词组".format(textcount))
    sentence='''北京欢迎你 北京怀疑你 北京欢迎您
    热烈庆祝火箭发射 热烈庆祝飞机发射 热烈庆祝北京发射
    '''.split()
    for i in sentence:
        print("{}的概率是{}".format(i,lang_mode(i,text,text_2,textcount,textcount_2,2)))

if __name__ == "__main__":
    main()
    # x=[1,2,3,4,1,2,3,1,2,1]
    # x=Counter(x)
    # print(x)