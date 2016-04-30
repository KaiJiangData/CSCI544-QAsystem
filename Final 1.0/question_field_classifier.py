# -*- coding: utf-8 -*-
import json
import codecs
import jieba
#function fieldClassify tackle with each question, you can just use this function.

class nbClassifier():
	def __init__(self):
		file = codecs.open("nbmodel_field.txt", 'r', 'utf-8')
		self.model_dict = {}
		line = file.read().splitlines()
		for i in xrange(0,len(line),3):
			key = line[i].split()[0]
			v1 = line[i].split()[1]
			v2 = line[i+1].split()[1]
			v3 = line[i+2].split()[1]
			self.model_dict[key] = [float(v1),float(v2),float(v3)]
		file.close()

	def fieldClassify(self,question):

		result = self.nbClassify(question, self.model_dict)
		return result

	def nbClassify(self,question_str, model_dict):
		from operator import add
		classifyArray = [0,0,0]
		question=question_str.split()
		for word in question:
			if model_dict.has_key(word):
				classifyArray = map(add, classifyArray, model_dict[word])
				summation = sum(classifyArray)
				classifyArray = [x - summation/3 for x in classifyArray]
		#Domestic
		if classifyArray[0] == max(classifyArray):
			return 1
		#International
		elif classifyArray[1] == max(classifyArray):
			return 0
		#Miltary
		elif classifyArray[2] == max(classifyArray):
			return 2
'''
file_domestic = codecs.open("testset_domestic.txt", 'r', 'utf-8').read()
file_international = codecs.open("testset_international.txt", 'r', 'utf-8').read()
file_miltary = codecs.open("testset_miltary.txt", 'r', 'utf-8').read()
'''
'''
nbc = nbClassifier()
print nbc.fieldClassify([u'埃及',u'旅游',u'部长',u'是',u'谁'])

for line in file_domestic.splitlines():
	print nbc.fieldClassify(line)
'''

