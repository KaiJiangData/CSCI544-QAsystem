# -*- coding: utf-8 -*-
import re
ques_info= {'field':'Inter',
            'type': 'Date',
            'info': ['巴希尔 · 法塔赫','劫机']
            }
# here only do segmentation, then match date pattern
# no stanford parsing here

# separate  analyze year and date here

candidates_month = []
candidates_year = []
art=open('test_seg.txt', 'rb').read().replace('\r','\\r').replace('\n','\\n').split(' ')

# justify if any date are qualified and if there is, add them to candidates
def select_month(art, a, b):
    for i in range(a, b):
        m =  re.search(r'(\d+\xE6\x9C\x88)', art[i]) # month
        if m != None:
            d =  re.search(r'(\d+\xE6\x97\xA5)',art[i+1]) # day
            if d!= None:
                candidates_month.append(m.group()+d.group())
            else:
                candidates_month.append(m.group())
    return candidates_month

def select_year(art, a, b):
    for i in range(a, b):
        y = re.search(r'(\d{4}\xE5\xB9\xB4)', art[i]) # year
        if y!=None:
            candidates_year.append(y.group())
    return candidates_year



for k in range(len(ques_info['info'])):
    for i in range(len(art)-20):
        if art[i].decode('utf-8')==ques_info['info'][k].decode('utf-8'):
            candidates_month = select_month(art, i-20, i+20)
            candidates_year = select_year(art, i-20, i+20)

print max(set(candidates_month), key=candidates_month.count)
print max(set(candidates_year), key=candidates_year.count)

# still need add one thing: if candidates_year is empty, then I use the year this article generated as year!!