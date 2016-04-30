Run Fast
=================================

CSCI544-QAsystem
----------------------------
###Final verson: 
https://www.dropbox.com/s/dsshhxmtph12ycf/querySystem.zip?dl=0

You can download final verson from the above dropBox link. 

However, in order to run this query system, you still need the corpus. 
The link of corpus is:https://www.dropbox.com/s/bxmlhwrccepxyol/Corpus.zip?dl=0

The articles inside the corpus should be imported to MongoDB.


Corg
### Description:
  Build a Chinese QA system giving people exact answers to queries instead of various web pages or documents for users to look up.

### Tools:
  Python, Java, Word segmentor from Stanford University

### Schedule:
__[2016/03/25 - 2016/03/29]__ discuss the task modules and tools (also the corresponding person) and work flow (with DDL)(must be tested on the feasibility); finish and submit the final proposal.

__[2016/03/29 - 2016/04/04]__ Start working! Give all feedbacks so we can still revise the modules, tasks and flow diagram;

__[2016/04/04 - 2016/04/21]__ Should have a working prototype by then;

__[2016/04/21 - 2016/04/28]__ Finish the final report and presentation; submit.
all DDL indicates 11:59pm that day.

### Resources:
  __[Useful course slides related]__ http://courses.washington.edu/ling573/SPR2014/slides/.
  
  __[book]__ https://helda.helsinki.fi/bitstream/handle/10138/21370/methodsf.pdf?sequence=2
  
  __[借鉴的框架论文]__ https://www.google.com/patents/US20020052871
  __[复旦nlp]__ https://github.com/xpqiu/fnlp
  
  大家觉得有用的资源都在这里贴上来，互相看看！

### Brief summary:
__[dataset]__:
1. Chinese Question classification dataset developed by Sudan University, very similar to TREC QA Dataset;

2. Questions and answers dataset from 4 large online discussion board in China; one question correspond to multiple answers from different people;

3. Three datasets from 3 sources that can be used to develop a word-segmentation and POS tagging problem; But we’re also looking for toolkit that can solve the problem more efficiently than simply building it by ourselves;

__[Target]__:
Build a Chinese QA system giving people exact answers instead of various web pages or documents for users to look up.

__[Method]__:
Build a word segmentation and POS tagging tool to help us extract key words/information and classify question types;
Using dataset1 to train a question classifier and get supertypes and subtypes of them, so we can give the desired answer a narrow limitation. For example, Q: where’s USC located in? This should be a info-asking question and we should limit our answer to a location name. Then we discompose the question and formulate again to get answers from Baidu/Bing(Google doesn’t work in China).
Connect Baidu/Bing API to extract and select answers to our new-formulated question. For example, Q: which year or date did 911 happen? We formulate a new question with key information and extract the most common date appears in the results from Baidu/Bing, since that could the most likely answer we want. Then return the answer(s) we generate to users.

__[Evaluation]__:
About the question part, we have dataset1 having correct types of multiple questions, so we can test on that. And for those subtypes who not showing on the dataset1 but we think should be added as a type, we’ll annotate questions manually;
About the answer accuracy part, we’ll test the system manually by selecting different questions of different types, and then manually judge if the answer is satisfying. We’ll use 2-3 people to score the same question also.
