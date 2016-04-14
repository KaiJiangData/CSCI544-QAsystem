#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import pymongo 
from pymongo import MongoClient
import time
import re

class artcile_search:

	def __init__(self):
		txtFile = [['fh_in_pos_2.txt'],['fh_ma_pos_2.txt'],['fh_mi_pos_2.txt']]
		self.db = [[],[],[]]

		client = MongoClient()
		db = client.processedProj
		self.mongodb={}
	
		for x in xrange(0,3,1):
			for i in xrange(0,len(txtFile[x]),1):
				collection = txtFile[x][i][0:9]
				self.mongodb[collection]=db[collection]
				line_number = 0
				with codecs.open(txtFile[x][i],'r','utf-8') as f:
					for line in f:
						if line_number%2==0:
							words = line.split()
							words.append(collection)
							self.db[x].append(words)
						else:
							self.db[x].append(line.split())
						line_number+=1

	def search(self,dic,db):
		lines=self.db[db]
		objectId=[]
		neededMatch=len(dic)
		for i in xrange(0,len(lines),2):
			match=0
			for word in lines[i+1]:
				if word in dic:
					match+=1
			if neededMatch==match:
				objectId.append(lines[i])
		return objectId

	def retrival(self,objectIdArr):
		num=[str(len(objectIdArr))]
		time=[]
		articles=[]
		for objectId in objectIdArr:
			res=self.mongodb[objectId[2]].find_one({'_id':objectId[1]})
			time.append(res['time'])
			articles+=re.split(u'[\u3002\uff1b\uff01\uff1f\n]#PU',res['article'])
		return num+time+articles

	def searchAndRetrival(self,dic,db):
		searchResult = self.search(dic,db)
		return self.retrival(searchResult)


				
# For debug

engine=artcile_search()
start_time = time.time()
res = engine.search(set([u'几内亚',u'海啸']),0)
art = engine.retrival(res)
print("--- %s seconds ---" % (time.time() - start_time))
print len(res)
print res
f=codecs.open('log.txt','w','utf-8')
for sentence in art:
	f.write(sentence+'\n')
f.close()




