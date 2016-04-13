# -*- coding: utf-8 -*-
# use info from question locate sentences
# distinguish name entities(syntactic parsing)
# can we just use the most commmon ci xing to do syntactic parsing?
# rank candidates and select one.(build a threshold if necessary)

# break articles to sentences
from itertools import repeat

'''
f= open('obama_sen.txt', 'wb')
for i in open('output_art.txt','rb').read().decode('utf-8').split('\n'):
    f.write(i.encode('utf-8')+'\n')
'''

# after parsing:
# simply count the most frequent NN as answer

ques_info= {'field':'Inter',
            'type': 'Person',
            'info': ['中央','财经','教授','教授']
            }
candidates=[]

art = str(open('sars_pars.txt', 'rb').read()).translate(None, ',.()\t\n').split(' ')
words = list(filter(('').__ne__, art))
for k in range(len(ques_info['info'])):
    for i in range(len(words)):
        if words[i].decode('utf-8')==ques_info['info'][k].decode('utf-8'):
            '''
            for j in range(i, len(words)):
                if words[j]=='NN':
                    candidates.append(words[j+1])
                    #if len(set(words[i-5:i+5]).intersection(ques_info['info']))>2:
                    #    candidates.extend(repeat(words[j+1], 3*len(set(words[i-5:i+5]).intersection(ques_info['info']))))# number of same elements between this sentence and my key words

                # set(a).intersection(b)
            '''
            for j in range(i, len(words)):
                #print words[j+12],words[j+10],words[j+11]
                if words[j]=='NN' or words[j]=='NR':
                    if words[j+1] in ques_info['info']:
                        #candidates.append(words[j+3])
                        if words[j+3]!='NN' or words[j]=='NR':
                            candidates.append(words[j+3])
                            #candidates.extend(repeat(words[j+3], 5))
                        else:
                            candidates.append(words[j+4])
                            #candidates.extend(repeat(words[j+4], 5))
                    else:
                        candidates.append(words[j+1])
                    break
for i in candidates:
    print i, 888

print max(set(candidates), key=candidates.count),999





# turn info in to bag of words:

# get the most nearby NN/NT candidates:

'''
for i in open('obama_parse.txt', 'rb').read().decode('utf-8').split('\n'):
    if i.find(u'NN')!=-1: # position of 'NN'
        b=''
        for k in range(i.find(u'NN')+3, len(i)):
            if i[k]==')':
                index=k
                break
            b+=i[k]
        print b

         #a.append(i[i.find(u'NN')+3:i.find(u'NN')+6]) # but i cant use three letters all the time right?!
'''