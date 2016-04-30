# -*- coding: utf-8 -*-
from __future__ import print_function
import operator
import re


class answer2:
	def __init__(self,_type,dic,bl):
		self.ques_info= {
			'type': _type,
			'info': dic,
			'block':bl
			}

		self.candidates_int={}
		self.candidates_dec={}
		self.candidates_month = {}
		self.candidates_year = {}
		self.candidates_per={}
		self.candidates_loc={}
	def select_int(self, words, tags,  a, b, weight):
		for i in range(a, b):
			y = re.match(u'\d+[^%\u6708\u65e5\u5e74]$', words[i]) # int
			if y!=None and tags[i]!='GPE' and words[i] not in self.ques_info['block']:
				#print(words[i])
				if words[i] in self.candidates_int:
					self.candidates_int[words[i]]+=weight*weight
				else:
					self.candidates_int[words[i]]=weight*weight


	def select_dec(self, words, tags,  a, b, weight):
		for i in range(a, b):
			
			y = re.match(r'^([+-]?\d+\.\d+)|(\d+\.?\d*%)$', words[i]) # decimal/percentage
			if y!=None and words[i] not in self.ques_info['block']:
				if words[i] in self.candidates_dec:
					self.candidates_dec[words[i]]+=weight*weight
				else:
					self.candidates_dec[words[i]]=weight*weight
			


	def select_month(self, words, tags,  a, b, weight):
		for i in range(a, b):
			m =  re.search(u'(\d+\u6708)', words[i]) # month
			if m != None:
				month = words[i]
				day=''
				if i != b-1:
					d =  re.search(u'(\d+\u65e5)',words[i+1]) # day
					if d!= None:
						day=words[i+1]
				monthAndDay = month+day
				
				if monthAndDay in self.candidates_month:
					self.candidates_month[monthAndDay]+=weight*weight
				else:
					self.candidates_month[monthAndDay]=weight*weight


	def select_year(self, words, tags,  a, b, weight):
		for i in xrange(a, b):
			y = re.search(u'(\d{4}\u5e74)', words[i]) # year
			if y!=None:
				if words[i] in self.candidates_year:
					self.candidates_year[words[i]]+=weight*weight
				else:
					self.candidates_year[words[i]]=weight*weight
			


	def select_per(self, words, tags,  a, b, weight):
		temp = []
		for i in xrange(a, b):
			if (tags[i]=='PERSON' or tags[i]=='NR') and words[i] not in self.ques_info['block']:
				if words[i] in self.candidates_per:
					self.candidates_per[words[i]]+=weight*weight
				else:
					self.candidates_per[words[i]]=weight*weight
				temp.append(words[i])
		return temp
	def p(self,s):
		for w in s:
			print(w,end='')
		print('')
	def select_loc(self, words, tags,  a, b, weight):
		temp = []
		for i in xrange(a, b):
			if tags[i]=='GPE' and words[i] not in self.ques_info['block']:
				#if words[i] == u'韩国':
				#	self.p(words)
				#	print(weight)
				if words[i] in self.candidates_loc:
					self.candidates_loc[words[i]]+=weight*weight
				else:
					self.candidates_loc[words[i]]=weight*weight
				temp.append(words[i])
		return temp

	def fun(self,arr):
		print('Im Thinking............')
		num_of_article = int(arr[0])
		arti_candi = []
		if self.ques_info['type']=='decimal':
			print('type decimal')
			self.candidates_dec={}
			info = self.ques_info['info']
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				key_match_set_article=set()
				set_candidates = set()

				for sen in xrange(len(arr[arti])):
					key_match_set_sentence=set()
					words=[]
					tags=[]
					wordtags=arr[arti][sen].split()
					for wordtag in wordtags:
						words.append(wordtag.rsplit('#',1)[0])
						tags.append(wordtag.rsplit('#',1)[1])

					punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
					punc.insert(0, 0)
					punc.append(len(words))
					for j in range(len(punc)-1):
						key_match_set_subSentence=set()
						for num in range(punc[j],punc[j+1]):
							if words[num] in info:
								key_match_set_subSentence.add(words[num])
								key_match_set_sentence.add(words[num])
								key_match_set_article.add(words[num])
						weight = len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)
						for key in key_match_set_subSentence:
							weight*=info[key]

						self.select_dec(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_dec(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)

			if self.candidates_dec!={}:
				print(max(self.candidates_dec.iteritems(), key=operator.itemgetter(1))[0])
			else:
				print('Sorry I dont know')



		if self.ques_info['type']=='integer':
			print('type integer')
			self.candidates_int={}
			info = self.ques_info['info']
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				key_match_set_article=set()
				set_candidates = set()

				for sen in xrange(len(arr[arti])):
					key_match_set_sentence=set()
					words=[]
					tags=[]
					wordtags=arr[arti][sen].split()
					for wordtag in wordtags:
						words.append(wordtag.rsplit('#',1)[0])
						tags.append(wordtag.rsplit('#',1)[1])

					punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
					punc.insert(0, 0)
					punc.append(len(words))
					for j in range(len(punc)-1):
						key_match_set_subSentence=set()
						for num in range(punc[j],punc[j+1]):
							if words[num] in info:
								key_match_set_subSentence.add(words[num])
								key_match_set_sentence.add(words[num])
								key_match_set_article.add(words[num])
						weight = len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)
						for key in key_match_set_subSentence:
							weight*=info[key]

						self.select_int(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_int(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)
			if self.candidates_int!={}:
				print(max(self.candidates_int.iteritems(), key=operator.itemgetter(1))[0])
			else:
				print('Sorry I dont know')


		if self.ques_info['type']=='time':
			print('type date')
			self.candidates_month={}
			self.candidates_year={}
			info = self.ques_info['info']
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				key_match_set_article=set()
				set_candidates = set()

				for sen in xrange(len(arr[arti])):
					key_match_set_sentence=set()
					words=[]
					tags=[]
					wordtags=arr[arti][sen].split()
					for wordtag in wordtags:
						words.append(wordtag.rsplit('#',1)[0])
						tags.append(wordtag.rsplit('#',1)[1])

					punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
					punc.insert(0, 0)
					punc.append(len(words))
					for j in range(len(punc)-1):
						key_match_set_subSentence=set()
						for num in range(punc[j],punc[j+1]):
							if words[num] in info:
								key_match_set_subSentence.add(words[num])
								key_match_set_sentence.add(words[num])
								key_match_set_article.add(words[num])
						weight = len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)*len(key_match_set_subSentence)
						for key in key_match_set_subSentence:
							weight*=info[key]

						self.select_month(words, tags, punc[j], punc[j+1], weight)
						self.select_year(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_month(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							self.select_year(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)

			
			if self.candidates_month!={} and self.candidates_year!={}:
				print(max(self.candidates_month.iteritems(), key=operator.itemgetter(1))[0]+max(self.candidates_year.iteritems(), key=operator.itemgetter(1))[0])
			elif self.candidates_year!={}:
				print(max(self.candidates_year.iteritems(), key=operator.itemgetter(1))[0])
			elif self.candidates_month!={}:
				b= []
				for i in arr[1:num_of_article+1]:
					b.append(i[:4])
				print(max(self.candidates_month.iteritems(), key=operator.itemgetter(1))[0]+max(set(b), key=b.count))
			else:
				print('Sorry I dont know')



		if self.ques_info['type']=='person':
			print('type person')
			self.candidates_per={}
			info = self.ques_info['info']
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				key_match_set_article=set()
				set_candidates = set()

				for sen in xrange(len(arr[arti])):
					key_match_set_sentence=set()
					words=[]
					tags=[]
					wordtags=arr[arti][sen].split()
					for wordtag in wordtags:
						words.append(wordtag.rsplit('#',1)[0])
						tags.append(wordtag.rsplit('#',1)[1])

					punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
					punc.insert(0, 0)
					punc.append(len(words))
					for j in range(len(punc)-1):
						key_match_set_subSentence=set()
						for num in range(punc[j],punc[j+1]):
							if words[num] in info:
								key_match_set_subSentence.add(words[num])
								key_match_set_sentence.add(words[num])
								key_match_set_article.add(words[num])
						weight = len(key_match_set_subSentence)*len(key_match_set_subSentence)
						for key in key_match_set_subSentence:
							weight*=info[key]

						self.select_per(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_per(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)
			if self.candidates_per!={}:
				print(max(self.candidates_per.iteritems(), key=operator.itemgetter(1))[0])
			else:
				print('Sorry I dont know')

		if self.ques_info['type']=='loc':
			print('type location')
			self.candidates_loc={}
			info = self.ques_info['info']
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				key_match_set_article=set()
				set_candidates = set()

				for sen in xrange(len(arr[arti])):
					key_match_set_sentence=set()
					words=[]
					tags=[]
					wordtags=arr[arti][sen].split()
					for wordtag in wordtags:
						words.append(wordtag.rsplit('#',1)[0])
						tags.append(wordtag.rsplit('#',1)[1])

					punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
					punc.insert(0, 0)
					punc.append(len(words))
					for j in range(len(punc)-1):
						key_match_set_subSentence=set()
						for num in range(punc[j],punc[j+1]):
							if words[num] in info:
								key_match_set_subSentence.add(words[num])
								key_match_set_sentence.add(words[num])
								key_match_set_article.add(words[num])
						if len(key_match_set_subSentence) > 0:
							weight = len(key_match_set_subSentence)*len(key_match_set_subSentence)
							for key in key_match_set_subSentence:
								weight*=info[key]
							self.select_loc(words, tags, punc[j], punc[j+1], weight)
					'''
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_loc(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)
					'''
					
			
			#print(self.candidates_loc)
			if self.candidates_loc!={}:
				print(max(self.candidates_loc.iteritems(), key=operator.itemgetter(1))[0])
			else:
				print('Sorry I dont know')