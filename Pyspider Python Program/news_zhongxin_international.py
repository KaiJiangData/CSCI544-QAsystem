import re
import pymongo
from pymongo import MongoClient
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    
    client = MongoClient()
    db = client.proj
    collection = db.news_zhongxin_international
 
    url1 = "http://www.chinanews.com/scroll-news/gj/"
    url2 = "/news.shtml"
    

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.chinanews.com/scroll-news/gj/2016/0330/news.shtml', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        
        for each in response.doc('.content_list a[href^="http"]').items():
            if re.match("http://www.chinanews.com\/gj\/\d{4}\/\d{2}\-\d{2}\S+.shtml", each.attr.href):
                self.crawl(each.attr.href, priority=9, callback=self.detail_page)
        
        url = response.url
        newdd = int(url[47:49])-1
        newmm = int(url[45:47])
        newyy = int(url[40:44])
        if(newdd==0):
            newmm-=1
            if(newmm==0):
                newyy-=1
                newmm=12
            if(newmm==2):
                newdd=28
            else:
                newdd=30
        yy=""
        mm=""
        dd=""
        if(newdd<10):
            dd="0"+str(newdd)
        else:
            dd=str(newdd)
        if(newmm<10):
            mm="0"+str(newmm)
        else:
            mm=str(newmm)
        yy=str(newyy)
        
        
        nextIndex = self.url1+yy+"/"+mm+dd+self.url2
            
        self.crawl(nextIndex, callback=self.index_page)
        
        

    def detail_page(self, response):
       
        arr=response.doc('.left_zw p').items()
        str=""
        for x in arr:
            str+=x.text()
        
        anews= {
            "keywords":response.doc('meta[name="keywords"]').attr('content'),
            "description":response.doc('meta[name=description]').attr('content'),
            "url":response.url,     
            "article":str,
            "title":response.doc('#cont_1_1_2 h1').text()
        }
        self.collection.insert_one(anews).inserted_id