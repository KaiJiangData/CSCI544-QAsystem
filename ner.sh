#!/bin/sh
scriptdir=`dirname $0`
java -mx700m -cp "$scriptdir/stanford-ner.jar:$scriptdir/lib/*:$scriptdir/stanford-chinese-corenlp-2015-12-08-models.jar" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier edu/stanford/nlp/models/ner/chinese.misc.distsim.crf.ser.gz -textFile $1
