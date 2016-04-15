# coding=UTF-8
###人:0,时间:1,地点:2,名词:3
import math

def tagQues(que, wordSet):
    tag =[0,0,0,0]
    for i in que:
        if wordSet.has_key(i):
            tag[0] = tag[0] + wordSet[i][0]
            tag[1] = tag[1] + wordSet[i][1]
            tag[2] = tag[2] + wordSet[i][2]
            tag[3] = tag[3] + wordSet[i][3]
    inx = tag.index(max(tag))
    print tag
    if inx == 0:
        tg = "人"
        return tg
    elif inx ==1:
        tg = "时间"
        return tg
    elif inx == 2:
        tg = "地点"
        return tg
    else:
        tg = "名词"
        return tg

if __name__ == '__main__':
    f1 = open("output.txt", "r")
    f2 = open("ques_classifier_training.txt","r")
    wordSet = {}
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    while True:
        s1 = f1.readline()
        s2 = f2.readline()
        if len(s1) == 0:
            break
        else:
            l1 = s1.split()
            l2 = s2.split('：')
            type = l2[1]
            type = type.strip('\n')
            if type == "人":
                for w in l1:
                    c1 = c1 + 1
                    if wordSet.has_key(w):
                        wordSet[w][0] = wordSet[w][0]+1
                    else:
                        wordSet[w] = [1,0,0,0]
            elif type == "时间":
                for w in l1:
                    c2 = c2 + 1
                    if wordSet.has_key(w):
                        wordSet[w][1] = wordSet[w][1] + 1
                    else:
                        wordSet[w] = [0, 1, 0, 0]
            elif type == "地点":
                for w in l1:
                    c3 = c3 + 1
                    if wordSet.has_key(w):
                        wordSet[w][2] = wordSet[w][2] + 1
                    else:
                        wordSet[w] = [0, 0, 1, 0]
            elif type == "名词":
                for w in l1:
                    c4 = c4 +1
                    if wordSet.has_key(w):
                        wordSet[w][3] = wordSet[w][3] + 1
                    else:
                        wordSet[w] = [0, 0, 0, 1]
    for i in wordSet:
        wordSet[i] = [wordSet[i][0]+1,wordSet[i][1]+1,wordSet[i][2]+1,wordSet[i][3]+1]
    for i in wordSet:
        wordSet[i] = [math.log(wordSet[i][0]/float(c1+len(wordSet))),math.log(wordSet[i][1]/float(c2+len(wordSet))),math.log(wordSet[i][2]/float(c3+len(wordSet))),math.log(wordSet[i][3]/float(c4+len(wordSet)))]

    test=["中国","生产","棉花","省"]
    tag=tagQues(test,wordSet)
    print tag



