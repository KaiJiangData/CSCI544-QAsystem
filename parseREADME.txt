Download http://nlp.stanford.edu/software/lex-parser.shtml#Download

1. Put addClassPath.sh, parseTxt.py and stanford-parser-full-2015-12-09 IN THE SAME directory.
2. Open lexparser_lang.def in stanford-parser-full-2015-12-09
   find -encoding for Chinese and change 'GB18030' to 'UTF-8'. After changing it should be like the following:

   elif [ $lang == "Chinese" ]; then
     tlp="$tlp".ChineseTreebankParserParams
     lang_opts="-chineseFactored -encoding UTF-8"

3. In the directory, run addClassPath.sh once for configuration by typing ./addClassPath.sh on terminal.
   This is to add class paths for java.
4. Usage: python parseTxt.py fileNeedsParse.txt outputFileName.txt
   NOTICE: the format of fileNeedsParse.txt must be:
   (1)each line is one sentence
   (2)each sentence has been segmented already