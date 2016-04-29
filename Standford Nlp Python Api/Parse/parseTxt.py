import sys
import os
import subprocess

command=["stanford-parser-full-2015-12-09/lexparser-lang.sh", "Chinese", "40", "edu/stanford/nlp/models/lexparser/xinhuaFactored.ser.gz",sys.argv[2],sys.argv[1]]
p = subprocess.Popen(command,shell=False)
p.wait()

os.rename(sys.argv[1]+"."+sys.argv[2]+".txt",sys.argv[2])


