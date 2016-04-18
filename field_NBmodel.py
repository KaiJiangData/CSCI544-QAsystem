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
    total = [0,0,0]
    dictDomestic = classifier("testset_domestic.txt", total, 0)
    dictInter = classifier("testset_international.txt", total, 1)
    dictMiltary = classifier("testset_miltary.txt", total, 2)
    # nbmodel is  the total dict of all classes
    nbmodel = {}
    defaultVal = [0,0,0]
    for i, val in enumerate(total):
        defaultVal[i] = - math.log(val,10) - 1

    for key in dictDomestic:
        nbmodel[key] = [dictDomestic[key], defaultVal[1], defaultVal[2]]
    for key in dictInter:
        if nbmodel.has_key(key):
            nbmodel[key][1]= dictInter[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],dictInter[key],defaultVal[2]])
    for key in dictMiltary:
        if nbmodel.has_key(key):
            nbmodel[key][2]= dictMiltary[key]
        else:
            nbmodel.setdefault(key,[defaultVal[0],defaultVal[1],dictMiltary[key]])
    string = ""
    #for i in nbmodel:
    #    string = string + i + str(nbmodel[i])+" "
    f = codecs.open("nbmodel_field.txt", 'w', 'utf-8')
    #f = open("nbmodel_field.txt", 'w',)
    #f.write(string)
    for k,v in nbmodel.iteritems():
        #print k,v
        for value in v:
            f.write(k+" "+ str(value)+'\n')

    f.close()



learning()










