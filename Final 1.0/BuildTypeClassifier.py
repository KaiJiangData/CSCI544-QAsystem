# -*- coding: utf-8 -*-
import json
import re
import codecs

#function fieldClassify tackle with each question, you can just use this function.
pattern_person = re.compile(ur"谁|哪位", re.UNICODE)
pattern_loc = re.compile(ur"在哪|哪.*(地|国|省|市|城|岛|山|湖|洋|河|海)", re.UNICODE)
pattern_time = re.compile(ur"什么时候|(什么|哪|几.*(年|月|日|天|朝代))", re.UNICODE)
pattern_integer = re.compile(ur"几任", re.UNICODE)
pattern_decimal = re.compile(ur"率", re.UNICODE)


class nbClassifier():
    def __init__(self):
        '''
        file = codecs.open("nbmodel_type.txt", 'r', 'utf-8')
        self.model_dict = {}
        line = file.read().splitlines()
        for i in xrange(0,len(line),5):
            key = line[i].split()[0]
            v1 = line[i].split()[1]
            v2 = line[i+1].split()[1]
            v3 = line[i+2].split()[1]
            v4 = line[i+3].split()[1]
            v5 = line[i+4].split()[1]
            self.model_dict[key] = [float(v1),float(v2),float(v3),float(v4),float(v5)]
        file.close()
        '''

    def fieldClassify(self,question):

        result = self.regexClassify(question)
        if result is not None:
            return result
        return 'person'
        # split question
        result = self.nbClassify(question, self.model_dict)
        return result

    def regexClassify(self,question):
        if pattern_person.search(question.decode('utf8')) is not None:
            return "person"
        elif pattern_loc.search(question.decode('utf8')) is not None:
            return "loc"
        elif pattern_time.search(question.decode('utf8')) is not None:
            return "time"
        elif pattern_integer.search(question.decode('utf8')) is not None:
            return "integer"
        elif pattern_decimal.search(question.decode('utf8')) is not None:
            return "decimal"
        else:
            return None

    def nbClassify(self,question_str, model_dict):
        from operator import add
        classifyArray = [0,0,0,0,0]
        question=question_str.split()
        for word in question:
            if model_dict.has_key(word):
                classifyArray = map(add, classifyArray, model_dict[word])
                summation = sum(classifyArray)
                classifyArray = [x - summation/5 for x in classifyArray]
        #person
        if classifyArray[0] == max(classifyArray):
            return 1
        #location
        elif classifyArray[1] == max(classifyArray):
            return 0
        #time
        elif classifyArray[2] == max(classifyArray):
            return 2
        #integer
        elif classifyArray[3] == max(classifyArray):
            return 3
        #decimal
        elif classifyArray[4] == max(classifyArray):
            return 4
'''
file_domestic = codecs.open("testset_domestic.txt", 'r', 'utf-8').read()
file_international = codecs.open("testset_international.txt", 'r', 'utf-8').read()
file_miltary = codecs.open("testset_miltary.txt", 'r', 'utf-8').read()

for line in file_domestic.splitlines():
    print nbc.fieldClassify(line)

nbc = nbClassifier()
print nbc.fieldClassify('埃及旅游部长是谁')
'''



