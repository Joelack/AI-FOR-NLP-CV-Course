import requests
import re
import requests.packages.urllib3.util.ssl_
import os
import sys
from collections import Counter

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

global dic_rude, dic_rude_ts, dic_ts, dic_ts_link,all_station,dic_rude_cycle
dic_rude={}#['1号线':['苹果园，公主坟']]每个线上的所有站点
dic_rude_ts={}#['1号线',[ 公主坟,军事博物馆,……]……]每个线上的所有换成站
dic_ts_rude={}#[军事博物馆:['1号线'，……]]换乘站连接的线路
dic_ts={}#[军事博物馆:[]]每个换乘站可以直接到达的站点
dic_ts_link={}#{'军事博物馆',[公主坟]每个换成站可直接到达的换成站
dic_rude_cycle=['1号线','10号线']
all_station=[]




def get_alldata():#爬虫获取所有线路和站点形成一个字典
    url = r"https://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"
    print('begin get data')
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.1) Gecko/20100101 Firefox/40.1', }
    text = requests.get(url, headers=header, timeout=6, verify=False).text
    #print(text)
    text = re.findall('> \w+</th>|>\w+</th>|\w+线.*首', text)
    #print(text)
    firstflage = True
    dic = {}
    for i in text:
        #print(i)
        if re.findall('时间|往|首车|末|全程|终点', i):
            continue
        if re.findall('\w+线.*首', i):
            if firstflage:
                x = re.findall('\w+线.*首', i)[0][:-1]
                y = []
                firstflage = not firstflage
            else:
                dic[x] = y
                x = re.findall('\w+线.*首', i)[0][:-1]
                y = []
            continue
        if re.findall('> \w+</th>|>\w+</th>', i):
            temp=re.findall('> \w+<|>\w+<', i)[0][1:-1]
            y.append(temp.strip())

    for i in dic:
        mailto = dic[i]
        addr_to = list(set(mailto))
        addr_to.sort(key=mailto.index)
        dic[i] = addr_to

        #print(len(dic[i]), i, dic[i])
    return dic

def get_subway_data():
    if "beijingsubway.txt"  not in os.listdir():
        dic=get_alldata()
        fw = open("beijingsubway.txt", 'w+')
        fw.write(str(dic))  # 把字典转化为str
        fw.close()
    else:
        fr = open("beijingsubway.txt", 'r+')
        dic = eval(fr.read())  # 读取的str转换为字典
        #print(dic)
        fr.close()
    return dic
def get_global_data(dic_rude):
    global dic_rude_ts, dic_ts, dic_ts_link, all_station, dic_rude_cycle
    all_station1= []
    for i in dic_rude:
        all_station1+=dic_rude[i]
    all_station=list(set(all_station1))
    all_station1=Counter(all_station1).most_common()#统计站点，重复两次为换成站
    all_ts=[ i for i,j in all_station1 if j>1]
    #print(all_ts)
    #计算dic_rude_ts
    for i in dic_rude:
        temp=[]
        for j in all_ts:
            if j in dic_rude[i]:temp.append(j)
        dic_rude_ts[i]=temp
    #计算dic_ts_rude dic_ts,dic_ts_link
    for i in all_ts:
        temptsrude=[]
        ts=[]
        link=[]
        for j in dic_rude:
            if i in dic_rude[j]:
                temptsrude.append(j)
                ts+=dic_rude[j]
                link+=dic_rude_ts[j]
        dic_ts_rude[i]=temptsrude
        temp= list(set(ts))
        temp.remove(i)
        dic_ts[i] =temp#.remove(i)
        temp=list(set(link))
        temp.remove(i)
        dic_ts_link[i]=temp

def count_station(start,des):#计算有几站路
    #不能直达返回-1
    #可以直达返回最小站数，和要做的线路
    result=[start,-1,des,'']#[苹果园 8站 军事博物馆 1号线]
    for i in dic_rude:
        if start in dic_rude[i] and des in dic_rude[i]:
            tempcount=abs(dic_rude[i].index(start)-dic_rude[i].index(des))
            if i in dic_rude_cycle:#是环线
                tempcount=len(dic_rude[i])-tempcount if len(dic_rude[i])-tempcount<tempcount else tempcount
            if result[1]<0 or tempcount<result[1]:
                result[1]=tempcount
                result[-1]=i
    return result
def count_all_rude_station(rude):#整条路线长度

    if len(rude)==1:return 0
    if len(rude) < 1: return -1
    return count_station(rude[0],rude[1])[1]+count_all_rude_station(rude[1:])
def say_all_rude_station(rude):#说明整条路线怎么走

    if len(rude)==1:return ''
    if len(rude) < 1: return '-1'
    res=count_station(rude[0],rude[1])
    return "从 {} 出发坐 {} 经过 {} 站到 {} 下车\n".format(res[0],res[-1],res[1],res[2])+say_all_rude_station(rude[1:])

def searchpath(start,des,stragegy):
    if start not in all_station:return '初始站点不存在'
    if des not in all_station:return '终点不存在'
    #是否在一条线上
    result=count_station(start,des)
    if result[1]>0:return result
    #初始站
    path=[]
    pathfinish=[]
    besearch={}#分层检索，后一层可以同时到达一个站点，但是不用检索前一层的站点
    if start not in dic_ts:
        for i in dic_rude:
            if start in dic_rude[i]:
                temp=[[start,j] for j in dic_rude_ts[i]]
                path.append(temp)
    else:
        path=[[[start]]]
    #print(besearch)
    while path[0]:
        Temp=[]
        temppath=path.pop()
        while temppath:
            temppathone=temppath.pop()
            laststation=temppathone[-1]
            if laststation in besearch and count_all_rude_station(temppathone)>besearch[laststation]:
                continue
            if des in dic_ts[laststation]:
                pathfinish.append(temppathone+[des])
                continue
            else:
                besearch[laststation]=count_all_rude_station(temppathone)
                for i in dic_ts_link[laststation]:
                    Temp.append(temppathone+[i])
        path.append(Temp)
    #print(pathfinish)
    if  stragegy=='shortts':#最少换成
        pathfinish=[i for i in pathfinish if len(i)==len(pathfinish[0])]
        sorted(pathfinish,key=count_all_rude_station)
    else:
        sorted(pathfinish, key=count_all_rude_station)

    print(say_all_rude_station(pathfinish[0]))

    return 0#没有找到路径

if __name__=="__main__":

    flagep=False
    dic_rude=get_subway_data()
    get_global_data(dic_rude)

    if flagep: print(dic_rude)
    if flagep: print(dic_rude_ts)
    if flagep: print(dic_ts)
    if flagep: print(dic_ts_rude)
    if flagep: print(dic_ts_link)
    if flagep: print(all_station)

    searchpath('北京西站', '知春路', stragegy='shorts')
