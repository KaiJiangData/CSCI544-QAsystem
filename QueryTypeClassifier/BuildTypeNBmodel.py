# coding=utf-8
import json
import os
import math
import extraction
import codecs
import sys

def classifier(Inputfile, total, index):# input path of different class, then output their dict
    dict={}
    # file = open(Inputfile, decode = 'utf-8','r')
    file = codecs.open(Inputfile, 'r', 'utf-8')
    for line in file:
        #article = json.loads(line, encoding="utf-8")["article"]
        #line = line.replace(u'：', "").replace(u'、', "").replace(u'？', "")
        #sentence = extraction.seg(article)
        for word in line.split():
            if dict.has_key(word):# check wether the dict contain the key "s"
                dict[word] += 1
            else: # added the key "s" and set the vaule to 1 if "s" not exist in dict.
                dict.setdefault(word,1)
    file.close()
    total[index] = sum(dict.values())
    for key, value in dict.items():
        dict[key] = math.log(float(value)/total[index], 10)
    return dict



def learning():
    total = [0,0,0,0,0]
    dictPerson = classifier("testset_person.txt", total, 0)
    dictLoc = classifier("testset_loc.txt", total, 1)
    dictTime = classifier("testset_time.txt", total, 2)
    dictInteger = classifier("testset_integer.txt", total, 3)
    dictDecimal = classifier("testset_decimal.txt", total, 4)
    # nbmodel is  the total dict of all classes
    nbmodel = {}
    defaultVal = [0,0,0,0,0]
    for i, val in enumerate(total):
        defaultVal[i] = - math.log(val,10) - 1

    for key in dictPerson:
        nbmodel[key] = [dictPerson[key], defaultVal[1], defaultVal[2],defaultVal[3],defaultVal[4]]
    for key in dictLoc:
        if nbmodel.has_key(key):
            nbmodel[key][1]= dictLoc[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],dictLoc[key],defaultVal[2],defaultVal[3],defaultVal[4]])
    for key in dictTime:
        if nbmodel.has_key(key):
            nbmodel[key][2]= dictTime[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],defaultVal[1],dictTime[key],defaultVal[3],defaultVal[4]])
    for key in dictInteger:
        if nbmodel.has_key(key):
            nbmodel[key][2]= dictInteger[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],defaultVal[1],defaultVal[2],dictInteger[key],defaultVal[4]])
    for key in dictDecimal:
        if nbmodel.has_key(key):
            nbmodel[key][2]= dictDecimal[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],defaultVal[1],defaultVal[2],defaultVal[3],dictDecimal[key]])

    f = codecs.open("nbmodel_type.txt", 'w', 'utf-8')
    for k,v in nbmodel.iteritems():
        #print k,v
        for value in v:
            f.write(k+" "+ str(value)+'\n')

    f.close()



learning()










