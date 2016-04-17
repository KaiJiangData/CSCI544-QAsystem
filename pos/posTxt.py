import sys
import os
import subprocess

#replace the original stanford-postagger.sh in stanford-postagger-full-2015-12-09 with the one I give
#Usage: python posTxt.py input.txt output.txt
command=["stanford-postagger-full-2015-12-09/stanford-postagger.sh", 'stanford-postagger-full-2015-12-09/models/chinese-distsim.tagger',sys.argv[1]]
pos_file = open(sys.argv[2], 'w')
p = subprocess.Popen(command, stdout=pos_file, shell=False)
p.wait()
pos_file.close()



