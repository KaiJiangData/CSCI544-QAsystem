# coding=UTF-8
import sys
import subprocess

class Question:
    def __init__(self, question, answer, type):
        # type: (object, object, object) -> object
        self.__question = question
        self.__answer = answer
        self.__type = type

    def setQue(self, question):
        self.__question = question

    def setAwr(self, answer):
        self.__answer = answer

    def setType(self, type):
        self.__type = type

    def setKeywords(self, key):
        self.__key = key

    def getKeywords(self):
        return self.__key


    def getQue(self):
        return self.__question

    def getAwr(self):
        return self.__answer

    def getType(self):
        return self.__type

    def printQ(self):
        s = self.__question + " answer: " + self.__answer + " : " + self.__type
        return s

def tokenization(inputfile,outputfile):
    command = ["./stanford-segmenter-2015-12-09/segment.sh", "ctb", inputfile, "UTF-8", "0"]
    segmented_file = open(outputfile, 'w')
    p = subprocess.Popen(command, stdout=segmented_file, shell=False)
    p.wait()
    segmented_file.close()

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    question = []
    while True:
        s = f.readline()
        if len(s) == 0 or len(s) == 1:
            break
        else:
            s1 = s.split('？')
            s2 = s1[1].split('：')
            if(len(s2)==2):
                q = Question(s1[0], s2[0], s2[1])
                question.append(q)
    f.close()
    tmp = open("input.txt", "w")
    for que in question:
        s=str(que.getQue())+'\n'
        tmp.write(s)
    tmp.close()
    tmp = open("output.txt", "w")
    tokenization("input.txt", "output.txt")
    f = open("output.txt","r")
    for que in question:
        s = f.readline().decode("utf-8")
        l = s.split()
        que.setKeywords(l)






