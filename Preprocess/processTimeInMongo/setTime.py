#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo 
from pymongo import MongoClient
import codecs
client = MongoClient()
db = client.processedProj
collection = db.zx_mi_pos
f=codecs.open('zx_mi_time.txt','r','utf-8')
lines = f.read().splitlines()
for line in lines:
	idTime = line.split()
	res=collection.update({'_id':idTime[0]},{'$set':{'time':idTime[1]}})

	