import sys
import re
import os
import codecs
import subprocess

# Put this segmentTxt.py and 'stanford-segmenter-2015-12-09' folder in the same directory
# 'stanford-segmenter-2015-12-09' folder that can be downloaded from http://nlp.stanford.edu/software/segmenter.shtml
# Usage: python segmentTxt.py input_Text_File_Name output_Text_File_Name

intermedia_buffer = "intermedia_buffer.txt"
command=["./stanford-segmenter-2015-12-09/segment.sh", "ctb", intermedia_buffer, "UTF-8","0"]

file_need_segment = open(sys.argv[1], "r")
content = file_need_segment.read().decode('utf-8')
file_need_segment.close()

split_content = re.split(u'[\u3002\uff1b\uff01\uff1f\n]',content)
intermedia_buffer_file = codecs.open(intermedia_buffer, 'w',"utf-8")
for line in split_content:
	if line==u"":
		continue
	intermedia_buffer_file.write(line)
	intermedia_buffer_file.write(u'\u3002')
	intermedia_buffer_file.write('\n')
intermedia_buffer_file.close()

segmented_file = open(sys.argv[2], 'w')
p = subprocess.Popen(command, stdout=segmented_file, shell=False)
p.wait()
segmented_file.close()
os.remove(intermedia_buffer)


