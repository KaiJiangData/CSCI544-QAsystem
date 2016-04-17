# -*- coding: utf-8 -*-
from __future__ import print_function
import operator
import re


class answer2:
	def __init__(self):
		self.ques_info= {'field':'Inter',
			'type': 'person',
			'info': [u'埃及', u'旅游', u'旅游',u'旅游',u'部长', u'部长', u'部长']
			}
		self.candidates_int=[]
		self.candidates_dec=[]
		self.candidates_month = []
		self.candidates_year = []
		self.candidates_per={}
	def select_int(self,art, a, b):
		for i in range(a, b):
			y = re.match(r'^-?\d+$', art[i]) # int
			if y!=None:
				self.candidates_int.append(y.group())
		return self.candidates_int

	def select_decimal(self,art, a, b):
		for i in range(a, b):
			y = re.match(r'^([+-]?\d+\.\d+)|(\d+\.?\d*%)$', art[i]) # decimal/percentage
			if y!=None:
				self.candidates_dec.append(y.group())
		return self.candidates_dec
	def select_month(self,art, a, b):
		for i in range(a, b):
			m =  re.search(r'(\d+\u6708)', art[i]) # month
			if m != None:
				d =  re.search(r'(\d+\u5929)',art[i+1]) # day
				if d!= None:
					self.candidates_month.append(m.group()+d.group())
				else:
					self.candidates_month.append(m.group())
		return self.candidates_month

	def select_year(self, art, a, b):
		for i in range(a, b):
			y = re.search(r'(\d{4}\u5e74)', art[i]) # year
			if y!=None:
				self.candidates_year.append(y.group())
		return self.candidates_year

	def select_per(self, words, tags,  a, b, weight):
		temp = []
		for i in xrange(a, b):
			if tags[i]=='PERSON' or tags[i]=='NR':
				if words[i] in self.candidates_per:
					self.candidates_per[words[i]]+=weight*weight
				else:
					self.candidates_per[words[i]]=weight*weight
				temp.append(words[i])
		return temp

	def select_loc(self, words, tags,  a, b, weight):
		temp = []
		for i in xrange(a, b):
			if tags[i]=='GPE':
				if words[i] in self.candidates_loc:
					self.candidates_loc[words[i]]+=weight*weight
				else:
					self.candidates_loc[words[i]]=weight*weight
				temp.append(words[i])
		return temp

	def fun(self,arr):
		num_of_article = int(arr[0])
		arti_candi = []
		if self.ques_info['type']=='decimal':

			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				for k in range(len(self.ques_info['info'])):
					whole_words=[]
					for sen in xrange(len(arr[arti])):
						words=[]
						wordtags=arr[arti][sen].split()
						for wordtag in wordtags:
							words.append(wordtag.rsplit('#',1)[0])
							whole_words.append(wordtag.rsplit('#',1)[0])

						try:
							punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
							punc.insert(0, 0)
							punc.append(len(words)-1)
							for num in range(len(words)):
								if words[num]==self.ques_info['info'][k]:
									for j in range(len(punc)):
										if num>punc[j] and num<punc[j+1]:
											candidates_dec = self.select_decimal(words, punc[j], punc[j+1])
						except ValueError:
							candidates_dec = self.select_decimal(words, 0, len(words)-1)
						for num in range(len(words)):
								if words[num]==self.ques_info['info'][k]:
									candidates_dec = self.select_decimal(words, 0, len(words)-1)
					if self.ques_info['info'][k] in whole_words:
						key_match+=1

				arti_candi.extend(max(set(candidates_dec), key=candidates_dec.count) for i in range(10*key_match))
			print (max(set(arti_candi), key=arti_candi.count))



		if self.ques_info['type']=='integer':
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				for k in range(len(self.ques_info['info'])):
					whole_words=[]
					for sen in xrange(len(arr[arti])):
						words=[]
						wordtags=arr[arti][sen].split()
						for wordtag in wordtags:
							words.append(wordtag.rsplit('#',1)[0])
							whole_words.append(wordtag.rsplit('#',1)[0])

						try:
							punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
							punc.insert(0, 0)
							punc.append(len(words)-1)
							for num in range(len(words)):
								if words[num]==self.ques_info['info'][k]:
									for j in range(len(punc)):
										if num>punc[j] and num<punc[j+1]:
											candidates_int = self.select_int(words, punc[j], punc[j+1])
						except ValueError:
							candidates_int = self.select_int(words, 0, len(words)-1)
						for num in range(len(words)):
								if words[num]==self.ques_info['info'][k]:
									candidates_int = self.select_int(words, 0, len(words)-1)
					if self.ques_info['info'][k] in whole_words:
						key_match+=1
				arti_candi.extend(max(set(candidates_int), key=candidates_int.count) for i in range(10*key_match))
			print (max(set(arti_candi), key=arti_candi.count))


		if self.ques_info['type']=='date':
			for arti in xrange(num_of_article+1, len(arr)):
				key_match=0
				for k in range(len(self.ques_info['info'])):
					whole_words=[]
					for sen in xrange(len(arr[arti])):
						words=[]
						wordtags=arr[arti][sen].split()
						for wordtag in wordtags:
							words.append(wordtag.rsplit('#',1)[0])
							whole_words.append(wordtag.rsplit('#',1)[0])

							for num in range(len(words)):
								if words[num]==self.ques_info['info'][k]:
									candidates_year = self.select_year(words, 0, len(words)-1)
									candidates_month = self.select_month(words, 0, len(words)-1)
					if self.ques_info['info'][k] in whole_words:
						key_match+=1

				if candidates_month!=[] and candidates_year!=[]:
					arti_candi.extend(max(set(candidates_month), key=candidates_month.count)+max(set(candidates_year), key=candidates_year.count) for i in range(10*key_match))
				elif candidates_month!=[]:
					b= []
					for i in arr[1:num_of_article+1]:
						b.append(i[0][:4])
					arti_candi.extend(max(set(candidates_month), key=candidates_month.count)+max(set(b), key=b.count) for i in range(10*key_match))
				else:
					b= []
					for i in arr[1:num_of_article+1]:
						b.append(i[0])
					arti_candi.extend(max(set(b), key=b.count) for i in range(10*key_match))
			print (max(set(arti_candi), key=arti_candi.count))


		if self.ques_info['type']=='person':
			self.candidates_per={}
			info = {}
			for w in self.ques_info['info']:
				if w not in info:
					info[w]=1
				else:
					info[w]+=1
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
							weight+=info[key]

						self.select_per(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_per(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)
			print(max(self.candidates_per.iteritems(), key=operator.itemgetter(1))[0])

		if self.ques_info['type']=='location':
			self.candidates_loc={}
			info = {}
			for w in self.ques_info['info']:
				if w not in info:
					info[w]=1
				else:
					info[w]+=1
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
							weight+=info[key]

						self.select_loc(words, tags, punc[j], punc[j+1], weight)
					infoCopy = dict(info)
					for num in range(len(words)):
						if words[num] in infoCopy:
							self.select_loc(words, tags, 0, len(words), infoCopy[words[num]]+len(key_match_set_sentence))
							infoCopy.pop(words[num],None)
			print(max(self.candidates_loc.iteritems(), key=operator.itemgetter(1))[0])