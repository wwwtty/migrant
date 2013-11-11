# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from utility import BaseHandler
from logic.news import NewsModel,hot,TName as TNews
from logic.category import TName as T_Category
from logic.utility import m_page
from logic.label import add as addlabel

@url(r'/news?')
class News(BaseHandler):
    def get(self):
        self.oneday = hot(5,1)
        self.weeknews = hot(5,7)
        self.monthnews = hot(5,30)
        r,self.categorys = m_page(T_Category,size=10)        
        news = {}
        for cate in self.categorys:
            r,news[cate.get('listname')] = m_page(TNews,category=cate.get('listname'))

        self.news = news
        self.render('action/news.html')


@url(r'/news/info/(.*)')
class NewsInfo(BaseHandler):
    def get(self,_id=None):
        self.render('action/newsinfo.html')

@url(r'/news/create')
class CreateNews(BaseHandler,NewsModel):
    def post(self):
        try:
            data = self._get_postdata(city=self.city)
            print data
            r,v = self._save(data)
            for i in data.get('labels',()):
                if i:
                    addlabel(3,i)

            self.write(dict(status=r,data=v)) 
        except Exception as e:
            self.write(e.message)

    def get(self):
        r,self.categorys = m_page(T_Category,size=10)        
        self.render('action/newssave.html')


