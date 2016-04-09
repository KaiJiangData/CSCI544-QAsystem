import sys
import os
import subprocess

#replace the original ner.sh in stanford-ner-2015-12-09 with the ner.sh I give
#if permission deny error, under stanford-ner-2015-12-09, type chmod 777 ner.sh on terminal  
#Usage: python nerTxt.py input.txt output.txt
command=["stanford-ner-2015-12-09/ner.sh", sys.argv[1]]
ner_file = open(sys.argv[2], 'w')
p = subprocess.Popen(command, stdout=ner_file, shell=False)
p.wait()
ner_file.close()



