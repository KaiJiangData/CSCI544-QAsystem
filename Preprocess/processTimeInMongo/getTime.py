#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo 
from pymongo import MongoClient
import codecs
import re

client = MongoClient()
db = client.project
collection = db.zx_mi
f=codecs.open('zx_mi_time.txt','w','utf-8')
'''
for d in collection.find():
	time = d['time'].split()
	if len(time) > 0:
		time_1=re.sub(u'[\u5e74\u6708]','-',time[0])
		time_2=re.sub(u'\u65e5','\n',time_1)
		f.write(str(d['_id'])+' '+time_2)
'''
'''
for d in collection.find():
	url = d['url']
	res=re.search('\d{4}-\d{2}-\d{2}',url)
	if res != None:
		f.write(str(d['_id'])+' '+res.group(0)+'\n')
f.close()
'''


for d in collection.find():
	url = d['url']
	res=re.search('\d{4}/\d{2}-\d{2}',url)
	if res != None:
		time=res.group(0)
		time_1 = re.sub('/','-',time)
		f.write(str(d['_id'])+' '+time_1+'\n')
f.close()
