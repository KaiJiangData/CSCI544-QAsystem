import re
import pymongo
from pymongo import MongoClient
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    
    #client = MongoClient()
    #db = client.proj
    #collection = db.news_fenghuang_international

        
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://news.ifeng.com/listpage/11574/20160330/1/rtlist.shtml', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        
        for each in response.doc('.newsList a[href^="http"]').items():
            if re.match("http:\/\/news.ifeng.com\/a\/\d+\/\S+.shtml", each.attr.href):
                self.crawl(each.attr.href, priority=9, callback=self.detail_page)
        arr= [x.attr.href for x in response.doc('.r_end > a').items()]
        self.crawl(arr[0], callback=self.index_page)
        
        

    def detail_page(self, response):
       
        arr=response.doc('#artical_real p').items()
        str=""
        for x in arr:
            str+=x.text()
        
        return {
            "keywords":response.doc('meta[name="keywords"]').attr('content'),
            "tags":response.doc('meta[name=tags]').attr('content'),
            "description":response.doc('meta[name=description]').attr('content'),
            "time":response.doc('meta[name="og:time"]').attr('content'),     
            "author":response.doc('meta[name="og:category "]').attr('content'),
            "article":str,
            "title":response.doc('meta[property="og:title"]').attr('content')
        }
        #self.collection.insert_one(anews).inserted_id
