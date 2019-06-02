#NLP Assignment 1:实现对话机器人
#根据输入句子提取语句中的关键词，然后根据关键词做正常应答
# 给定一种规则如{'?*x I feel ?*y': ['Do you often feel ?y ?', 'What other feelings do you have?'],}
#输入Jack I feel headache
#输出Do you often feel headache ?或者What other feelings do you have?

#1  首先要做匹配，将输入和规则进行匹配然后找到对应的规则。
#2  查找并提取关键字
#3  根据关键字返回数据

#代码反向实现
def is_variable(pat):#查看某个是不是关键字：单匹配
    return pat.startswith('?') and all(a.isalpha() for a in pat[1:]) and pat[1:]
def is_variable_s(pat):#查看某个是不是关键字:多匹配
    return pat.startswith('?*') and all(a.isalpha() for a in pat[2:])

def getmatchcount(pat,saying):
    if not pat or not saying:return len(saying)+1
    if pat[0] not in saying:return len(saying)
    else: return saying.index(pat[0])+1

def pat_match(pattern,saying):#根据输入查看是否匹配
    #print(pattern,saying)
    if not pattern and not saying:return[]   #两者同时结束返回True匹配完成
    if not pattern or not saying:return [False]   #其中一个结束另一个没有结束返回Fals
    if is_variable(pattern[0]):
        return [(pattern[0],saying[0])]+pat_match(pattern[1:],saying[1:])
    if is_variable_s(pattern[0]):#需要知道匹配了几个
        k = getmatchcount(pattern[1:], saying[1:])
        return [(pattern[0], ' '.join(saying[:k]))]+pat_match(pattern[1:], saying[k:])
    if pattern[0] != saying[0]:return  [False]
    else:return pat_match(pattern[1:],saying[1:])
#笔记 a=[1,2,4] a+[]=[1,2,3]

#print(pat_match('?x is very good ?*y yes he is'.split(),'Lili is very good my big cat yes he is'.split()))
#print(pat_match('?*x I was ?*y'.split(),'Jim Green I was Ttuolasiji pi'.split()))

#处理汉子字符
def dealchr(tk):
    k=''
    i=0
    while i<len(tk):
        if tk[i:i+2]=='?*' and tk[i+2:i+3].isalpha():
            k=k+tk[i:i+3]+' '
            i+=3
            continue;
        if tk[i:i+1]=='?' and tk[i+1:i+2].isalpha():
            k=k+tk[i:i+2]+' '
            i+=2
            continue;
        else:
            k = k + tk[i:i+1] + ' '
            i += 1
    return k.strip()
#print(dealchr('?*x你好?*y'))

import random
#输入应答规则
def respond(rules,saying):
    flage=all(ord(x)<256 for x in saying)
    if not flage : saying=dealchr(saying)
    for k in rules:
        k1=k
        #print(k.split(), saying.split())
        if not flage:
            if all(ord(x)<256 for x in k):continue;
            k=dealchr(k)
        dic=pat_match(k.split(), saying.split())
        #print(dic)
        if False not in dic:
            # 做应答并返回
            dic={p:t for p,t in dic}
            res=[]
            if flage:
                resp=random.choice(rules[k1]).split()
            else:
                resp = dealchr(random.choice(rules[k1])).split()

            for k1 in resp:
                if is_variable(k1):
                    res.append(dic.get('*'.join(k1),k1))
                    continue
                res.append(k1)
            if flage:
                return ' '.join(res)
            else:
                return ''.join(res).replace(' ','')

    return 'I don\'t understand, say others'
rule_responses = {
    '?*x hello ?*y': ['How do you do', 'Please state your problem'],
    '?*x I want ?*y': ['what would it mean if you got ?y', 'Why do you want ?y', 'Suppose you got ?y soon'],
    '?*x if ?*y': ['Do you really think its likely that ?y', 'Do you wish that ?y', 'What do you think about ?y', 'Really-- if ?y'],
    '?*x no ?*y': ['why not?', 'You are being a negative', 'Are you saying \'No\' just to be negative?'],
    '?*x I was ?*y': ['Were you really', 'Perhaps I already knew you were ?y', 'Why do you tell me you were ?y now?'],
    '?*x I feel ?*y': ['Do you often feel ?y ?', 'What other feelings do you have?'],
    '?*x你好?*y': ['你好呀', '请告诉我你的问题'],
    '?*x我想?*y': ['你觉得?y有什么意义呢？', '为什么你想?y', '你可以想想你很快就可以?y了'],
    '?*x我想要?*y': ['?x想问你，你觉得?y有什么意义呢?', '为什么你想?y', '?x觉得... 你可以想想你很快就可以有?y了', '你看?x像?y不', '我看你就像?y'],
    '?*x喜欢?*y': ['喜欢?y的哪里？', '?y有什么好的呢？', '你想要?y吗？'],
    '?*x讨厌?*y': ['?y怎么会那么讨厌呢?', '讨厌?y的哪里？', '?y有什么不好呢？', '你不想要?y吗？'],
    '?*xAI?*y': ['你为什么要提AI的事情？', '你为什么觉得AI要解决你的问题？'],
    '?*x机器人?*y': ['你为什么要提机器人的事情？', '你为什么觉得机器人要解决你的问题？'],
    '?*x对不起?*y': ['不用道歉', '你为什么觉得你需要道歉呢?'],
    '?*x我记得?*y': ['你经常会想起这个吗？', '除了?y你还会想起什么吗？', '你为什么和我提起?y'],
    '?*x如果?*y': ['你真的觉得?y会发生吗？', '你希望?y吗?', '真的吗？如果?y的话', '关于?y你怎么想？'],
    '?*x我?*z梦见?*y':['真的吗? --- ?y', '你在醒着的时候，以前想象过?y吗？', '你以前梦见过?y吗'],
    '?*x妈妈?*y': ['你家里除了?y还有谁?', '嗯嗯，多说一点和你家里有关系的', '她对你影响很大吗？'],
    '?*x爸爸?*y': ['你家里除了?y还有谁?', '嗯嗯，多说一点和你家里有关系的', '他对你影响很大吗？', '每当你想起你爸爸的时候， 你还会想起其他的吗?'],
    '?*x我愿意?*y': ['我可以帮你?y吗？', '你可以解释一下，为什么想?y'],
    '?*x我很难过，因为?*y': ['我听到你这么说， 也很难过', '?y不应该让你这么难过的'],
    '?*x难过?*y': ['我听到你这么说， 也很难过',
                 '不应该让你这么难过的，你觉得你拥有什么，就会不难过?',
                 '你觉得事情变成什么样，你就不难过了?'],
    '?*x就像?*y': ['你觉得?x和?y有什么相似性？', '?x和?y真的有关系吗？', '怎么说？'],
    '?*x和?*y都?*z': ['你觉得?z有什么问题吗?', '?z会对你有什么影响呢?'],
    '?*x和?*y一样?*z': ['你觉得?z有什么问题吗?', '?z会对你有什么影响呢?'],
    '?*x我是?*y': ['真的吗？', '?x想告诉你，或许我早就知道你是?y', '你为什么现在才告诉我你是?y'],
    '?*x我是?*y吗': ['如果你是?y会怎么样呢？', '你觉得你是?y吗', '如果你是?y，那一位着什么?'],
    '?*x你是?*y吗':  ['你为什么会对我是不是?y感兴趣?', '那你希望我是?y吗', '你要是喜欢， 我就会是?y'],
    '?*x你是?*y' : ['为什么你觉得我是?y'],
    '?*x因为?*y' : ['?y是真正的原因吗？', '你觉得会有其他原因吗?'],
    '?*x我不能?*y': ['你或许现在就能?*y', '如果你能?*y,会怎样呢？'],
    '?*x我觉得?*y': ['你经常这样感觉吗？', '除了到这个，你还有什么其他的感觉吗？'],
    '?*x我?*y你?*z': ['其实很有可能我们互相?y'],
    '?*x你为什么不?*y': ['你自己为什么不?y', '你觉得我不会?y', '等我心情好了，我就?y'],
    '?*x好的?*y': ['好的', '你是一个很正能量的人'],
    '?*x嗯嗯?*y': ['好的', '你是一个很正能量的人'],
    '?*x不嘛?*y': ['为什么不？', '你有一点负能量', '你说 不，是想表达不想的意思吗？'],
    '?*x不要?*y': ['为什么不？', '你有一点负能量', '你说 不，是想表达不想的意思吗？'],
    '?*x有些人?*y': ['具体是哪些人呢?'],
    '?*x有的人?*y': ['具体是哪些人呢?'],
    '?*x某些人?*y': ['具体是哪些人呢?'],
    '?*x每个人?*y': ['我确定不是人人都是', '你能想到一点特殊情况吗？', '例如谁？', '你看到的其实只是一小部分人'],
    '?*x所有人?*y': ['我确定不是人人都是', '你能想到一点特殊情况吗？', '例如谁？', '你看到的其实只是一小部分人'],
    '?*x总是?*y': ['你能想到一些其他情况吗?', '例如什么时候?', '你具体是说哪一次？', '真的---总是吗？'],
    '?*x一直?*y': ['你能想到一些其他情况吗?', '例如什么时候?', '你具体是说哪一次？', '真的---总是吗？'],
    '?*x或许?*y': ['你看起来不太确定'],
    '?*x可能?*y': ['你看起来不太确定'],
    '?*x他们是?*y吗？': ['你觉得他们可能不是?y？'],
    '?*x': ['很有趣', '请继续', '我不太确定我很理解你说的, 能稍微详细解释一下吗?']
}
for i in range(20):print(respond(rule_responses,'老师我想换NLP'))
for i in range(20):print(respond(rule_responses,'Teacher I feel CV hard') )







