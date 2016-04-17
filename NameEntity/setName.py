#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo 
from pymongo import MongoClient
import codecs
import sys
filename=sys.argv[1]
inputFile = codecs.open(filename, 'r','utf-8')
lines = inputFile.read().splitlines()
inputFile.close()
dic={}
for line in lines:
	nametag = line.split()
	name = nametag[0]
	tag=nametag[1]
	dic[name]=tag

client = MongoClient()
db = client.processedProj
collection = db[filename[0:5]+'_pos']

for d in collection.find():
	_id=d['_id']
	wordtags=d['article'].split()
	newArticle=''
	for wordtag in wordtags:
		word = wordtag.rsplit('#',1)[0]
		tag = wordtag.rsplit('#',1)[1]
		if dic.has_key(word):
			newArticle+=(word+'#'+dic[word]+' ')
		else:
			newArticle+=(wordtag+' ')
	collection.update({'_id':_id},{'$set':{'article':newArticle.rstrip(' ')}})





