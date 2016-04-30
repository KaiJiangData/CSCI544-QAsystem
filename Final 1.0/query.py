#!/usr/bin/env python
# -*- coding: utf-8 -*-

import search
import codecs
import ans8
import query_preprocess
import question_field_classifier
import BuildTypeClassifier

engine=search.artcile_search()
processQ = query_preprocess.processQuery()
classifier = question_field_classifier.nbClassifier()
typeclassifier = BuildTypeClassifier.nbClassifier()

while True:
	print 'Input a query'
	userInput=raw_input()
	if userInput=='q':
		break 

	queryType = typeclassifier.fieldClassify(userInput)
	#queryType = 'person' #time

	processQ.processQueryPos(userInput)
	info = processQ.extractFineInfo(queryType)
	block = processQ.block()
	wordSet = processQ.extractSearchInfo()
	database = classifier.fieldClassify(processQ.segQuery)
	database = 0

	res = engine.search(wordSet,database)
	art = engine.retrival(res)

	ans = ans8.answer2(queryType,info,block)
	ans.fun(art)



	
