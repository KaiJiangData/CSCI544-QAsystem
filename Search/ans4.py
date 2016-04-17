# -*- coding: utf-8 -*-
from __future__ import print_function
import re

class answer2:
    def __init__(self):
        self.ques_info= {'field':'Inter',
            'type': 'person',
            'info': [u'四',u'四', u'四', u'四']
            }
        self.candidates_int=[]
        self.candidates_dec=[]
        self.candidates_month = []
        self.candidates_year = []
        self.candidates_per=[]
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

    def select_per(self, words, tags,  a, b):
        for i in range(a, b):
            if tags[i]=='NR':
                self.candidates_per.append(words[i])
        

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
                    # havent add the influence of key_match yet

        if self.ques_info['type']=='person' or self.ques_info['type']=='location':
            for arti in xrange(num_of_article+1, len(arr)):
                self.candidates_per=[]
                key_match=0
                for k in range(len(self.ques_info['info'])):
                    whole_words=[]
                    for sen in xrange(len(arr[arti])):
                        words=[]
                        tags=[]
                        wordtags=arr[arti][sen].split()
                        for wordtag in wordtags:
                            words.append(wordtag.rsplit('#',1)[0])
                            tags.append(wordtag.rsplit('#',1)[1])
                            whole_words.append(wordtag.rsplit('#',1)[0])

                        try:
                            punc = [x for x in range(len(words)) if words[x]==u'\uFF0C']
                            punc.insert(0, 0)
                            punc.append(len(words)-1)
                            for num in range(len(words)):
                                if words[num]==self.ques_info['info'][k]:
                                    for j in range(len(punc)):
                                        if num>punc[j] and num<punc[j+1]:
                                            self.select_per(words, tags, punc[j], punc[j+1])
                        except ValueError:
                            self.select_per(words,tags, 0, len(words)-1)
                        for num in range(len(words)):
                            if words[num]==self.ques_info['info'][k]:
                                self.select_per(words, tags, 0, len(words)-1)
                    if self.ques_info['info'][k] in whole_words:
                        key_match+=1
                for i in self.candidates_per:
                    if i in self.ques_info['info']:
                        self.candidates_per.remove(i)
                if self.candidates_per!=[]:
                    
                    #print (max(set(self.candidates_per), key=self.candidates_per.count))
                    arti_candi.extend(max(set(self.candidates_per), key=self.candidates_per.count) for i in range(key_match*key_match*key_match))
                    '''
                    for a in arti_candi:
                        print (a,' ', end='')
                    print ('')
                    print ('_________________')
                    '''
            print (max(set(arti_candi), key=arti_candi.count))


    def toArr(self):
        # change this part!!
        #art=open('log3.txt', 'rb').readlines()
        # art change into [[num],[time],[time],[[sen1],[sen2]], [[sen1],[sen2]]]
        return art

