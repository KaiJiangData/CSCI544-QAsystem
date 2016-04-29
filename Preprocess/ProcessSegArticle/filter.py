#!/usr/bin/env python
import codecs
import sys


inputPath=sys.argv[1]
outputPath=sys.argv[2]
inputFile=codecs.open(inputPath,'r','utf-8')
lines = inputFile.read().splitlines()

outputFile=codecs.open(outputPath,'w','utf-8')

id=''
article=''
for line in lines:
	wordTagPairs = line.split()
	wordTag1 = wordTagPairs[0].rsplit('#',1)
	if wordTag1[0]=='ObjectId':
		if article!='' and id != '':
			outputFile.write('ObjectId '+id+'\n')
			outputFile.write(article+'\n')
		id=''
		article=''
		for i in xrange(1,len(wordTagPairs)-1,1):
			wordTag = wordTagPairs[i].rsplit('#',1)
			id+=wordTag[0]
	else:
		line+=" "
		article+=line

inputFile.close()
outputFile.close()
