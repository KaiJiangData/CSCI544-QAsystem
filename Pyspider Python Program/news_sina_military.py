import re
import pymongo
from pymongo import MongoClient
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    
    client = MongoClient()
    db = client.proj
    collection = db.news_sina_military_v2

        
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://roll.mil.news.sina.com.cn/col/zgjq/index_1.shtml', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        
        for each in response.doc('.main a[href^="http"]').items():
            if re.match("http:\/\/mil.news.sina.com.cn\S*\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])/\S+.s?html", each.attr.href):
                self.crawl(each.attr.href, priority=9, callback=self.detail_page)
        arr= [x.attr.href for x in response.doc('.pagebox_next > a').items()]
        self.crawl(arr[0], callback=self.index_page)
        

    def detail_page(self, response):
       
        arr=response.doc('.content p').items()
        str=""
        for x in arr:
            str+=x.text()
        
        anews = {
            "keywords":response.doc('meta[name=keywords]').attr('content'),
            "tags":response.doc('meta[name=tags]').attr('content'),
            "description":response.doc('meta[name=description]').attr('content'),
            "time":response.doc('meta[property="article:published_time"]').attr('content'),  
            "author":response.doc('meta[property="article:author"]').attr('content'),
            "article":str,
            "titile":response.doc('meta[property="og:title"]').attr('content'),
        }
        news_id = self.collection.insert_one(anews).inserted_id