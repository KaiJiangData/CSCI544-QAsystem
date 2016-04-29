#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys



inputPath=sys.argv[1]
outputPath=sys.argv[2]
inputFile=codecs.open(inputPath,'r','utf-8')
lines = inputFile.read().splitlines()

outputFile=codecs.open(outputPath,'w','utf-8')

for i in xrange(0,len(lines),2):
	id=lines[i]
	article=lines[i+1]
	wordTagPairs=article.split()
	filteredWordTagPairs=[]
	wordSet = set()
	for j in xrange(0,len(wordTagPairs),1):
		wordTag=wordTagPairs[j].rsplit('#',1)
		if wordTag[1]=='NR' or wordTag[1]=='NN':
			#withTag
			#filteredWordTagPairs.append(wordTagPairs[j])
			#withoutTag
			filteredWordTagPairs.append(wordTag[0])
			wordSet.add(wordTag[0])


	# without removing duplicated
	'''
	if len(filteredWordTagPairs) > 0:
		newArticle = filteredWordTagPairs[0]
		for x in xrange(1,len(filteredWordTagPairs),1):
			newArticle+=(" "+filteredWordTagPairs[x])
		outputFile.write(id+'\n')
		outputFile.write(newArticle+'\n')
	'''
	

	if len(wordSet) > 0:
		newArticle=''
		for word in wordSet:
			newArticle+=(word+' ')
		#newArticle=newArticle[:-1]
		outputFile.write(id+'\n')
		outputFile.write(newArticle+'\n')
	
inputFile.close()
outputFile.close()


