#!/bin/sh
#
# usage: ./stanford-postagger.sh model textFile
#  e.g., ./stanford-postagger.sh models/english-left3words-distsim.tagger sample-input.txt

java -mx300m -cp 'stanford-postagger-full-2015-12-09/stanford-postagger.jar:stanford-postagger-full-2015-12-09/lib/*' edu.stanford.nlp.tagger.maxent.MaxentTagger -model $1 -textFile $2
