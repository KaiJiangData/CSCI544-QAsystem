#!/usr/bin/env python
# -*- coding: utf-8 -*-
import search
import codecs
import ans8
import FieldClassifierAndKeywords


engine=search.artcile_search()
while True:
	print 'Input a query'
	userInput=raw_input()
	if userInput=='q':
		break 
	s = FieldClassifierAndKeywords.FieldClassifierAndKeywords(userInput)
	_type=s[0]
	mySearchSet = set()
	dictInfo = {}
	for var in s[1]:
		mySearchSet.add(var.decode('utf-8'))
	for var in s[2]:
		dictInfo[var.decode('utf-8')] = int(s[2][var])
		
	res = engine.search(mySearchSet,0)
	art = engine.retrival(res)

	ans = ans8.answer2(_type,dictInfo)
	ans.fun(art)

	
