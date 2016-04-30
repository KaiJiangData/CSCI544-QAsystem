#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import pymongo 
from pymongo import MongoClient

dicNR={}
dicNN={}
txtFile = ['fh_in_pos.txt','si_in_pos.txt','zx_in_pos.txt']
total=0
for filename in txtFile:
	inputFile=codecs.open(filename,'r','utf-8')
	lines = inputFile.read().splitlines()
	inputFile.close()
	total+=len(lines)/2
	for i in xrange(0,len(lines),2):
		id=lines[i]
		article=lines[i+1]
		wordTagPairs=article.split()
		findedNR=set()
		findedNN=set()
		for j in xrange(0,len(wordTagPairs),1):
			wordTag=wordTagPairs[j].rsplit('#',1)
			if wordTag[1]=='NR' and wordTag[0] not in findedNR:
				if wordTag[0] not in dicNR:
					dicNR[wordTag[0]]=0
				dicNR[wordTag[0]]+=1
				findedNR.add(wordTag[0])
			if wordTag[1]=='NN' and wordTag[0] not in findedNN:
				if wordTag[0] not in dicNN:
					dicNN[wordTag[0]]=0
				dicNN[wordTag[0]]+=1
				findedNN.add(wordTag[0])

print total
out1=codecs.open('in_nr.txt','w','utf-8')
for key in dicNR:
	if dicNR[key]>=total*0.2:
		out1.write(key+' NR '+str(dicNR[key])+'\n')
out1.close()

out1=codecs.open('in_nn.txt','w','utf-8')
for key in dicNN:
	if dicNN[key]>=total*0.1:
		out1.write(key+' NN '+str(dicNN[key])+'\n')
out1.close()




