# -*- coding: utf-8 -*-
import json
import extraction
import codecs
#function fieldClassify tackle with each question, you can just use this function.
def fieldClassify(question):
    #question = extraction.seg(question)
    file = codecs.open("nbmodel_field.txt", 'r', 'utf-8')
    model_dict = {}
    line = file.read().splitlines()
    for i in xrange(0,len(line),3):
        key = line[i].split()[0]
        v1 = line[i].split()[1]
        v2 = line[i+1].split()[1]
        v3 = line[i+2].split()[1]
        model_dict[key] = [float(v1),float(v2),float(v3)]

    #model_dict = json.loads(f.read())
    result = nbClassify(question, model_dict)
    return result

def nbClassify(question, model_dict):
    from operator import add
    classifyArray = [0,0,0]
    for word in question:
        if model_dict.has_key(word):
            classifyArray = map(add, classifyArray, model_dict[word])
            summation = sum(classifyArray)
            classifyArray = [x - summation/3 for x in classifyArray]
    if classifyArray[0] == max(classifyArray):
        return "Domestic"
    elif classifyArray[1] == max(classifyArray):
        return "International"
    elif classifyArray[2] == max(classifyArray):
        return "Miltary"

file_domestic = codecs.open("testset_domestic.txt", 'r', 'utf-8').read()
file_international = codecs.open("testset_international.txt", 'r', 'utf-8').read()
file_miltary = codecs.open("testset_miltary.txt", 'r', 'utf-8').read()


for line in file_domestic.splitlines():
    print fieldClassify(line)

