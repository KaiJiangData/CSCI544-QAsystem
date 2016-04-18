#coding=utf-8
import sys
import os
import subprocess
import jieba
import string
import re
import math
import json
import codecs
import time
import json

class FieldClassifierAndKeywords:

    def __init__(self):
        words = jieba.cut("我是谁", cut_all=False)


    def FieldClassifierAndKeywords(self,question):
    ##读入问题,调用分词工具分词,同时去除标点符号
        delset = string.punctuation
        question = question.translate(None, delset)
        questionTag = self.typeClassify(question)
        f = open("input.txt","w")
        words = jieba.cut(question, cut_all = False)
        s = ""
        for i in words:
            s = s+i.encode('utf-8')+" "
        f.write(s)
        f.close()
        command = ["stanford-postagger-full-2015-12-09/stanford-postagger.sh",
                   'stanford-postagger-full-2015-12-09/models/chinese-distsim.tagger', "input.txt"]
        pos_file = open("output.txt", 'w')
        p = subprocess.Popen(command, stdout=pos_file, shell=False)
        p.wait()
    ##s就是pos后的question
        pos_file.close()
        f = codecs.open("output.txt","r")
        s = f.readline().strip()
        Keywords = self.extract(s)
        #KeywordsWithWeight = keywordWeight(s)
        kw = self.keyweight(s)
        return [questionTag,Keywords,kw]

        pattern_person = re.compile(ur"谁|哪位", re.UNICODE)
        pattern_time = re.compile(ur"什么时候|(哪|几.*(年|月|日|天|朝代))", re.UNICODE)
        pattern_loc = re.compile(ur"哪.*(地|国|省|市|城|岛|山|湖|洋|河|海)", re.UNICODE)
        pattern_integer = re.compile(ur"几任", re.UNICODE)
        pattern_decimal = re.compile(ur"率|比例", re.UNICODE)

    # question types: Name, Location, Time, Other
    def typeClassify(self,question):
        # Use regex to classify
        result = self.regexClassify(question)
        if result is not None:
            return result
        words = jieba.cut(question, cut_all = False)
        ques=[]
        for i in words:
            ques.append(i)
        t1 = time.time()
        result = self.nbClassifier(ques)
        t2 = time.time() - t1
        print t2
        return result



    def tagQues(self,que,wordSet):
        tag =[0,0,0,0]
        for i in que:
            i = i.encode("utf-8")
            if wordSet.has_key(i):
                tag[0] = tag[0] + wordSet[i][0]
                tag[1] = tag[1] + wordSet[i][1]
                tag[2] = tag[2] + wordSet[i][2]
                tag[3] = tag[3] + wordSet[i][3]
        inx = tag.index(max(tag))
        if inx == 0:
            tg = "人"
            return tg
        elif inx ==1:
            tg = "时间"
            return tg
        elif inx == 2:
            tg = "地点"
            return tg
        else:
            tg = "名词"
            return tg

    def nbClassifier(self,question):
        f1 = open("out-put.txt", "r")
        f2 = open("ques_classifier_training.txt","r")
        wordSet = {}
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        while True:
            s1 = f1.readline()
            s2 = f2.readline()
            if len(s1) == 0:
                break
            else:
                l1 = s1.split()
                l2 = s2.split('：')
                type = l2[1]
                type = type.strip('\n')
                if type == "人":
                    for w in l1:
                        c1 = c1 + 1
                        if wordSet.has_key(w):
                            wordSet[w][0] = wordSet[w][0]+1
                        else:
                            wordSet[w] = [1,0,0,0]
                elif type == "时间":
                    for w in l1:
                        c2 = c2 + 1
                        if wordSet.has_key(w):
                            wordSet[w][1] = wordSet[w][1] + 1
                        else:
                            wordSet[w] = [0, 1, 0, 0]
                elif type == "地点":
                    for w in l1:
                        c3 = c3 + 1
                        if wordSet.has_key(w):
                            wordSet[w][2] = wordSet[w][2] + 1
                        else:
                            wordSet[w] = [0, 0, 1, 0]
                elif type == "名词":
                    for w in l1:
                        c4 = c4 +1
                        if wordSet.has_key(w):
                            wordSet[w][3] = wordSet[w][3] + 1
                        else:
                            wordSet[w] = [0, 0, 0, 1]
        for i in wordSet:
            wordSet[i] = [wordSet[i][0]+1,wordSet[i][1]+1,wordSet[i][2]+1,wordSet[i][3]+1]
        for i in wordSet:
            wordSet[i] = [math.log(wordSet[i][0]/float(c1+len(wordSet))),math.log(wordSet[i][1]/float(c2+len(wordSet))),math.log(wordSet[i][2]/float(c3+len(wordSet))),math.log(wordSet[i][3]/float(c4+len(wordSet)))]
        #fout = open("wordSet.txt","w")
        #s= json.dumps(wordSet)
        #fout.write(s)
        #fout.close()
        tag=self.tagQues(question,wordSet)
        return tag



    def regexClassify(self,question):
        if self.pattern_person.search(question.decode('utf8')) is not None:
            return "person"
        elif self.pattern_loc.search(question.decode('utf8')) is not None:
            return "loc"
        elif self.pattern_time.search(question.decode('utf8')) is not None:
            return "time"
        elif self.pattern_integer.search(question.decode('utf8')) is not None:
            return "integer"
        elif self.pattern_decimal.search(question.decode('utf8')) is not None:
            return "decimal"
        else:
            return None

    def target(self,question):
        if self.pattern_person.search(question.decode('utf8')) is not None\
            or self.pattern_loc.search(question.decode('utf8')) is not None:
            return "name"
        elif self.pattern_integer.search(question.decode('utf8')) is not None \
                or self.pattern_decimal.search(question.decode('utf8')) is not None:
            return "quantity"
        elif self.pattern_time.search(question.decode('utf8')) is not None:
            return "time"
        else:
            return None


    def nbClassify(self,question, model_dict):
        from operator import add
        classifyArray = [0,0,0,0]
        for word in question.spilt(' '):
            if model_dict.has_key(word):
                classifyArray = map(add, classifyArray, model_dict[word])
                summation = sum(classifyArray)
                classifyArray = [x - summation/4 for x in classifyArray]
        if classifyArray[0] == max(classifyArray):
            return "person"
        elif classifyArray[1] == max(classifyArray):
            return "loc"
        elif classifyArray[2] == max(classifyArray):
            return "time"
        elif classifyArray[3] == max(classifyArray):
            return "other"

    def extract(self,question):
        keywords = set()
        for word in question.split():
            sep = word.split('#')
            word = sep[0]
            tag = sep[1]
            if tag[0] == 'N':
                keywords.add(word)
        return keywords




    def keywordWeight(self,question):
        keyword = []
        f = codecs.open("chinese_stopwords.txt","r","utf-8")
        stopWord ={}
        while True:
            s = f.readline()
            if len(s) ==0:
                break
            else:
                s= s.strip("\r\n")
                stopWord[s] = 1
        for word in question.split():
            sep = word.split('#')
            word = sep[0].decode("utf-8")
            tag = sep[1]
            if stopWord.has_key(word):
                continue
            else:
                if tag[0] =='N':
                    keyword.append(word)
                else:
                    keyword.append(word)
                    keyword.append(word)
        return keyword


    def keyweight(self,question):
        words = []
        tag = []
        for word in question.split():
            sep = word.split('#')
            words.append(sep[0])
            tag.append(sep[1])
        f = open("tagwithweight.txt","r")
        pairs = json.loads(f.read())
        finaltagWeights = []
        for i in pairs:
            f =False
            if len(i[0]) != len(tag):
                continue
            for n in range(0,len(i[0])):
                #print i[0][n]
                #print tag[n]
                if i[0][n] == tag[n]:
                    f = True
                else:
                    f = False
                    break
            if f == True:
                finaltagWeights = i[1]
                break
        key = {}
        for i in range(0,len(finaltagWeights)):
            if finaltagWeights[i] == 0:
                continue
            else:
                key[words[i]] = finaltagWeights[i]
        return key



if __name__ == '__main__':
    s = FieldClassifierAndKeywords("越南第十三届国会第十一次会议什么时候举办?")
    s1 = s[0].decode('utf-8')
    print s1
    for i in s[1]:
        print i
    for i in s[2]:
        print i + str(s[2][i])

