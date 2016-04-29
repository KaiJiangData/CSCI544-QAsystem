#!/usr/bin/env python
import pymongo 
from pymongo import MongoClient
import codecs

client = MongoClient()
db = client.project
collection = db.fh_ma
f=codecs.open('fh_ma.txt','w','utf-8')
for d in collection.find():
	
	f.write('ObjectId '+str(d['_id']))
	f.write('\n')
	f.write(d['article'])
	f.write('\n')
	
f.close()