
# -*- coding: utf-8 -*-
import re
class answer2:
    def __init__(self):
        self.ques_info= {'field':'Inter',
            'type': 'person',
            'info': ['四', '地震', '四', '四', '四']
            }
        self.candidates_int=[]
        self.candidates_dec=[]
        self.candidates_month = []
        self.candidates_year = []
        self.candidates_per=[]
    def select_int(self,art, a, b):
        for i in range(a, b):
            y = re.match(r'^-?\d+$', art[i]) # int
            if y!=None:
                self.candidates_int.append(y.group())
        return self.candidates_int

    def select_decimal(self,art, a, b):
        for i in range(a, b):
            y = re.match(r'^([+-]?\d+\.\d+)|(\d+\.?\d*%)$', art[i]) # decimal/percentage
            if y!=None:
                self.candidates_dec.append(y.group())
        return self.candidates_dec
    def select_month(self,art, a, b):
        for i in range(a, b):
            m =  re.search(r'(\d+\xE6\x9C\x88)', art[i]) # month
            if m != None:
                d =  re.search(r'(\d+\xE6\x97\xA5)',art[i+1]) # day
                if d!= None:
                    self.candidates_month.append(m.group()+d.group())
                else:
                    self.candidates_month.append(m.group())
        return self.candidates_month

    def select_year(self, art, a, b):
        for i in range(a, b):
            y = re.search(r'(\d{4}\xE5\xB9\xB4)', art[i]) # year
            if y!=None:
                self.candidates_year.append(y.group())
        return self.candidates_year

    def select_per(self, words, tags,  a, b):
        for i in range(a, b):
            if tags[i]=='NR':
                self.candidates_per.append(words[i])
        return self.candidates_per

    def fun(self,arr):
        num_of_article = int(arr[0])
        if self.ques_info['type']=='decimal':
            for k in range(len(self.ques_info['info'])):
                for sen in xrange(num_of_article+1,len(arr),1):
                    words=[]
                    wordtags=arr[sen].split(' ')
                    for wordtag in wordtags:
                        words.append(wordtag.rsplit('#',1)[0])

                    # 先分句(假设不同句那肯定就不是我们要找的),然后利用逗号信息,这里只利用了逗号
                    try:
                        # 逗号的index # 再加个首尾
                        punc = [x for x in range(len(words)) if words[x]=='，']
                        punc.insert(0, 0)
                        punc.append(len(words)-1)
                        for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                for j in range(len(punc)):
                                    if num>punc[j] and num<punc[j+1]:
                                        candidates_dec = self.select_decimal(words, punc[j], punc[j+1])
                    except ValueError:
                        candidates_dec = self.select_decimal(words, 0, len(words)-1)
                    # 这部分就是给比如2013年这种整句的限制,也考虑进去.以上的部分删除了他的影响.
                    for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                candidates_dec = self.select_decimal(words, 0, len(words)-1)
            print max(set(candidates_dec), key=candidates_dec.count)

        if self.ques_info['type']=='integer':
            for k in range(len(self.ques_info['info'])):
                for sen in xrange(num_of_article+1,len(arr),1):
                    words=[]
                    wordtags=arr[sen].split()
                    for wordtag in wordtags:
                        words.append(wordtag.rsplit('#',1)[0])

                    # 先分句(假设不同句那肯定就不是我们要找的),然后利用逗号信息,这里只利用了逗号
                    try:
                        # 逗号的index # 再加个首尾
                        punc = [x for x in range(len(words)) if words[x]=='，']
                        punc.insert(0, 0)
                        punc.append(len(words)-1)
                        for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                for j in range(len(punc)):
                                    if num>punc[j] and num<punc[j+1]:
                                        candidates_int = self.select_int(words, punc[j], punc[j+1])
                    except ValueError:
                        candidates_int = self.select_int(words, 0, len(words)-1)
                    # 这部分就是给比如2013年这种整句的限制,也考虑进去.以上的部分删除了他的影响.
                    for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                candidates_int = self.select_int(words, 0, len(words)-1)
            print max(set(candidates_int), key=candidates_int.count)

        if self.ques_info['type']=='date':
            for k in range(len(self.ques_info['info'])):
                for sen in xrange(num_of_article+1,len(arr),1):
                    words=[]
                    wordtags=arr[sen].split()
                    for wordtag in wordtags:
                        words.append(wordtag.rsplit('#',1)[0])

                        for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                candidates_year = self.select_year(words, 0, len(words)-1)
                                candidates_month = self.select_month(words, 0, len(words)-1)
            if candidates_month!=[] and candidates_year!=[]:
                print max(set(candidates_month), key=candidates_month.count)+max(set(candidates_year), key=candidates_year.count)
            # here 没有找到时间的话就会用该文章的时间作参考
            elif candidates_month!=[]:
                print "I'm not sure of the year...Maybe this one?"
                b= []
                for i in arr[1:num_of_article+1]:
                    b.append(i[0][:4])
                print max(set(candidates_month), key=candidates_month.count)+max(set(b), key=b.count)
            else:
                print "I'm not sure really...I'm purely guessing here: "
                b= []
                for i in arr[1:num_of_article+1]:
                    b.append(i[0])
                print max(set(b), key=b.count)

        if self.ques_info['type']=='person' or self.ques_info['type']=='location':
            for k in range(len(self.ques_info['info'])):
                for sen in xrange(num_of_article+1,len(arr),1):
                    words=[]
                    tags=[]
                    wordtags=arr[sen].split()
                    for wordtag in wordtags:
                        words.append(wordtag.rsplit('#',1)[0])
                        tags.append(wordtag.rsplit('#',1)[1])

                    try:
                        # 逗号的index # 再加个首尾
                        punc = [x for x in range(len(words)) if words[x]=='，']
                        punc.insert(0, 0)
                        punc.append(len(words)-1)
                        for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                for j in range(len(punc)):
                                    if num>punc[j] and num<punc[j+1]:
                                        candidates_per = self.select_per(words, tags, punc[j], punc[j+1])
                    except ValueError:
                        candidates_per = self.select_per(words,tags, 0, len(words)-1)
                    for num in range(len(words)):
                            if words[num].decode('utf-8')==self.ques_info['info'][k].decode('utf-8'):
                                candidates_per = self.select_per(words, tags, 0, len(words)-1)
            for i in candidates_per:
                if i in self.ques_info['info']:
                    candidates_per.remove(i)
            if candidates_per!=[]:
                print max(set(candidates_per), key=candidates_per.count)
            else:
                print "Sorry... I really don't know..."


    def toArr(self):
        art=open('log3.txt', 'rb').readlines()
        return art


ans = answer2()
ans.fun(ans.toArr())