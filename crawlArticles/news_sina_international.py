import re
import pymongo
from pymongo import MongoClient
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    
    #client = MongoClient()
    #db = client.proj
    #collection = db.news_sina_international_v2

        
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_90.shtml', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        
        for each in response.doc('.listBlk a[href^="http"]').items():
            if re.match("http\:\/\/news.sina.com.cn\/[a-z\/]+\/\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])\/\S+.shtml", each.attr.href):
                self.crawl(each.attr.href, priority=9, callback=self.detail_page)
        arr= [x.attr.href for x in response.doc('.pagebox_next > a').items()]
        self.crawl(arr[0], callback=self.index_page)
        

    def detail_page(self, response):
       
        arr=response.doc('#artibody p').items()
        str=""
        for x in arr:
            str+=x.text()
        
        return {
            "keywords":response.doc('meta[name=keywords]').attr('content'),
            "tags":response.doc('meta[name=tags]').attr('content'),
            "description":response.doc('meta[name=description]').attr('content'), 
            "url":response.url,
            "article":str,
            "title":response.doc('#artibodyTitle').text(),
        }
        #news_id = self.collection.insert_one(anews).inserted_id
