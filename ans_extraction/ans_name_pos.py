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
            'info': ['加拿大','坠毁','飞机','遇难','遇难']
            }
candidates=[]

words = str(open('test_pos.txt', 'rb').read()).translate(None, '\n').replace('#', ' ').split(' ')

# words = list(filter(('').__ne__, art))
for k in range(len(ques_info['info'])):
    for i in range(len(words)):
        if words[i].decode('utf-8')==ques_info['info'][k].decode('utf-8'):
            for j in range(i-10, i+10):
                #print words[j+12],words[j+10],words[j+11]
                if words[j]=='NR':
                    if words[j-1] not in ques_info['info']:
                        if j <i:
                            for a in range(j,i):
                                if words[a]!='PU':
                                    candidates.append(words[j-1])
                        else:
                            for a in range(i,j):
                                if words[a]!='PU':
                                    candidates.append(words[j-1])
# here i use -10 ~10distance, and make nouns without PU heavier than with PU
for i in candidates:
    print i, 888

print max(set(candidates), key=candidates.count),999
