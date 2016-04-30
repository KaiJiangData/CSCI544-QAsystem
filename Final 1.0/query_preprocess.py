# -*- coding: utf-8 -*-
#!/usr/bin/env python
import jieba
import os
import codecs
import subprocess

class processQuery:
	def __init__(self):
		self.segment('载入分词程序')
		os.system('clear')
		self.posQuery=''
		self.segQuery=''

	def segment(self,str):
		seg_list = jieba.cut(str,cut_all=True)
		return ' '.join(seg_list)

	def processQueryPos(self, unicodeQuery):
		utf8Query = unicodeQuery.decode('utf-8')
		forseg=codecs.open('forseg.txt', 'w', 'utf-8')
		forseg.write(utf8Query)
		forseg.close()
		command=["./stanford-segmenter-2015-12-09/segment.sh", "ctb", 'forseg.txt', "UTF-8","0"]
		print "start segment"
		segmented_file = codecs.open('segmentQuery.txt', 'w', 'utf-8')
		devnull = open('/dev/null', 'w')
		p = subprocess.Popen(command, stdout=segmented_file, shell=False,stderr=devnull)
		p.wait()
		segmented_file.close()

		command=["stanford-postagger-full-2015-12-09/stanford-postagger.sh", 'stanford-postagger-full-2015-12-09/models/chinese-distsim.tagger','segmentQuery.txt']
		posQueryFile = codecs.open('posQueryFile.txt', 'w', 'utf-8')
		print "start pos"
		p = subprocess.Popen(command, stdout=posQueryFile, shell=False,stderr=devnull)
		p.wait()
		posQueryFile.close()
		devnull.close()

		posQueryFile = codecs.open('posQueryFile.txt', 'r', 'utf-8')
		posQuery = posQueryFile.read().splitlines()
		self.posQuery = posQuery[0]

		wordTags=posQuery[0].split()
		for wordTag in wordTags:
			self.segQuery+=wordTag.rsplit('#',1)[0]+' '
		self.segQuery.rstrip(' ')

	def processQueryPosFast(self, unicodeQuery):
		utf8Query = unicodeQuery.decode('utf-8')
		segmentQueryFile=codecs.open('segmentQuery.txt', 'w', 'utf-8')
		self.segQuery = self.segment(utf8Query)
		segmentQueryFile.write(self.segQuery)
		segmentQueryFile.close()

		command=["stanford-postagger-full-2015-12-09/stanford-postagger.sh", 'stanford-postagger-full-2015-12-09/models/chinese-distsim.tagger','segmentQuery.txt']
		posQueryFile = codecs.open('posQueryFile.txt', 'w', 'utf-8')
		devnull = open('/dev/null', 'w')
		p = subprocess.Popen(command, stdout=posQueryFile, shell=False,stderr=devnull)
		p.wait()
		posQueryFile.close()
		devnull.close()

		posQueryFile = codecs.open('posQueryFile.txt', 'r', 'utf-8')
		posQuery = posQueryFile.read().splitlines()
		self.posQuery = posQuery[0]

	def extractSearchInfo(self):
		words=set()
		wordTags=self.posQuery.split()
		for i in xrange(0,len(wordTags),1):
			wordTag=wordTags[i].rsplit('#',1)
			if wordTag[1]=='NN' or wordTag[1]=='NR' or wordTag[1]=='VV' or wordTag[1]=='VA':
				words.add(wordTag[0])
		return words

	def extractFineInfo(self,_type):
		wordTags=self.posQuery.split()
		words=[]
		tags=[]
		for wordTag in wordTags:
			words.append(wordTag.rsplit('#',1)[0])
			tags.append(wordTag.rsplit('#',1)[1])
		VV = -1;
		for i in xrange(len(tags)-1,-1,-1):
			if tags[i]=='VV' or tags[i]=='VA':
				VV=i
				break;

		count=0;
		flag=True
		for i in xrange(len(tags)-1,-1,-1):
			#print words[i]+' '+tags[i]
			if flag == True:
				if tags[i]=='NN' or tags[i]=='NR':
					count+=1
					flag=False
			else:
				if tags[i]!='NN' and tags[i]!='NR':
					flag=True
		#print count

		info={}
		if count==1:
			weight=[1,2,3]
		elif count==2:
			weight=[1,3]
		else:
			weight=[1]

		point = len(weight)-1
		for i in xrange(len(tags)-1,-1,-1):
			if tags[i]=='NN' or tags[i]=='NR':
				if point!=-1:
					info[words[i]]=weight[point]
					point-=1
			else:
				point = len(weight)-1
				

		if VV != -1:
			info[words[VV]]=2
			if _type == 'loc':
				info[words[VV]]=10

		if _type == 'decimal' or _type == 'integer':
			duoshao=-1
			for i in xrange(0,len(tags),1):
				if words[i]==u'多少':
					duoshao=i
					break
			if duoshao!=-1 and duoshao!=len(words)-1 and tags[duoshao+1]!='PU':
				info[words[duoshao+1]]=5

		return info

	def block(self):
		blockedWords=set()
		wordTags=self.posQuery.split()
		for i in xrange(0,len(wordTags),1):
			wordTag=wordTags[i].rsplit('#',1)
			blockedWords.add(wordTag[0])
		return blockedWords

'''
processQ = processQuery()
processQ.processQueryPos(raw_input())
print processQ.posQuery
print processQ.segQuery


info = processQ.extractFineInfo('loc')
for w in info:
	print w+' '+str(info[w])
'''






