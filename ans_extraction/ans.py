# -*- coding: utf-8 -*-
import re
'''
ques_info= {'field':'Inter',
            'target':'Name',
            'type': 'Person',
            'info': ['奥巴马','母亲','母亲']
            }
'''
# articles=[[num],[time1],[time2],[time3], [sen1], [sen2], [sen3]......[sen1999]]

class answer(object):
    def __init__(self, target, type, info, articles, candidates=[]):
        self.target=target
        self.type=type
        self.info=info
        self.articles=articles
        self.candidates=candidates
    def select(self, type, words, a, b):
        if type=='integer':
            for i in range(a, b):
                y = re.match(r'^-?\d+$', words[i]) # int
                if y!=None:
                    self.candidates.append(y.group())
        if type=='decimal':
            for i in range(a, b):
                y = re.match(r'^([+-]?\d+\.\d+)|(\d+\.?\d*%)$', words[i]) # decimal/percentage
                if y!=None:
                    self.candidates.append(y.group())
        if type=='date':
            # 月日的部分
            self.candidates=[[],[]]
            for i in range(a, b):
                m =  re.search(r'(\d+\xE6\x9C\x88)', words[i]) # month
                if m != None:
                    d =  re.search(r'(\d+\xE6\x97\xA5)',words[i+1]) # day
                    if d!= None:
                        self.candidates[0].append(m.group()+d.group())
                    else:
                        self.candidates[0].append(m.group())
            for i in range(a, b):
                y = re.search(r'(\d{4}\xE5\xB9\xB4)', words[i]) # year
                    if y!=None:
                        self.candidates[1].append(y.group())
        if type=='person' or 'location':
            for i in range(a, b):
                if words[i][-2:]=='NR':# 于是这也显示有bug???
                    self.candidates.append(words[i][:-3])



    def output(self, type, info, articles):
        start_point=articles[0]
        if type=='integer' or 'decimal':
            for k in range(len(info)):
                for sen in articles[start_point+1:]:
                    words=[x[:-3] for x in sen.split(' ')]
            # 先分句(假设不同句那肯定就不是我们要找的),然后利用逗号信息,这里只利用了逗号
                    try:
                        punc = [x for x in range(len(words)) if words[x]=='，']
                        punc.insert(0, 0)
                        punc.append(len(words)-1)
                        for num in range(len(words)):
                            if words[num].decode('utf-8')==info[k].decode('utf-8'):
                                for j in range(len(punc)):
                                    if num>punc[j] and num<punc[j+1]:
                                        self.candidates.append(self.select(type, words, punc[j], punc[j+1]))
                    except ValueError:
                        self.candidates.append(self.select(type, words, 0, len(words)-1))
            # 这部分就是给比如2013年这种整句的限制,也考虑进去.以上的部分删除了他的影响.
                    for num in range(len(words)):
                            if words[num].decode('utf-8')==info[k].decode('utf-8'):
                                self.candidates.append(self.select(type, words, 0, len(words)-1))
            if self.candidates!=[]:
                return max(set(self.candidates), key=self.candidates.count)
            else:
                return 'sorry buddy, just google it.'
        if type=='date':
            for k in range(len(info)):
                for sen in articles[start_point+1:]:
                    words=sen.split(' ')# we must fix the POS problem! all tags should be two digits
                    for word in words:
                        if word.decode('utf-8')==info[k].decode('utf-8'):
                            self.candidates.append(self.select(type, words, 0, len(words)-1))
            if self.candidates[0]!=[] and self.candidates[1]!=[]:
                return max(set(self.candidates[0]), key=self.candidates[0].count)+max(set(self.candidates[1]), key=self.candidates[1].count)
            # here 再加一个缺少时间的判断!
            else:
                return 'sorry buddy, just google it.'
        if type=='person' or 'location':
            # we still need POS to distinguish these two
            for k in range(len(info)):
                for sen in articles[start_point+1:]:
                    words=sen.split(' ')
            # 先分句(假设不同句那肯定就不是我们要找的),然后利用逗号信息,这里利用了所有tag成PU的符号
                    try:
                        punc = [x for x in range(len(words)) if words[x][-2:]=='PU']
                        punc.insert(0, 0)
                        punc.append(len(words)-1)
                        for num in range(len(words)):
                            if words[num][:-3].decode('utf-8')==info[k].decode('utf-8'):
                                for j in range(len(punc)):
                                    if num>punc[j] and num<punc[j+1]:
                                        self.candidates.append(self.select(type, words, punc[j], punc[j+1]))
                    except ValueError:
                        self.candidates.append(self.select(type, words, 0, len(words)-1)
            # 这部分就是给比如2013年这种整句的限制,也考虑进去.以上的部分删除了他的影响.

                    for num in range(len(words)): # 这里咋回事..显示有bug...
                        if words[num][:-3].decode('utf-8')==info[k].decode('utf-8'):
                            self.candidates.append(self.select(type, words, 0, len(words)-1))
                if k in self.candidates:
                    self.candidates.remove(k) # delete key words themselves
            if self.candidates!=[]:
                return max(set(self.candidates), key=self.candidates.count)
            else:
                return 'sorry buddy, just google it.'


