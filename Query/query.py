#!/usr/bin/env python
# -*- coding: utf-8 -*-
import search
import codecs
import jieba

class query:
	def __init__(self):
		self.engine=search.artcile_search()

def segment(str):
	seg_list = jieba.cut(str)  
	return ' '.join(seg_list)


startQuery = query()
segment('载入分词程序')

while True:
	userInput=raw_input().decode('utf-8')
	if userInput=='q':
		break 
	retrivalArticles = startQuery.engine.searchAndRetrival(set(userInput.split()),0)
	