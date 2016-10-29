#-*- coding:utf-8 -*-


import urllib.parse
import requests

from bs4 import BeautifulSoup

class Book(object):
    """
        Get book info by specifying a name
    """

    def __init__(self,name):
        self.name=name

    def detail(self):

        detail=self.search(self.name)
        return detail


    def search(self,name):

        return self._do_search_from_douban(name)


    def _do_search_from_douban(self,search_text):

        api="https://book.douban.com/subject_search?search_text="+search_text+"&cat=1001"
        data=requests.get(api)
        soup=BeautifulSoup(data.text,"html.parser")
        book_list=soup.find_all(attrs={"class":"subject-item"})
        book_info=book_list[0]
        pic=book_info.img['src']
        pub=book_info.find(attrs={"class":"pub"}).get_text().strip()
        rating_nums=book_info.find(attrs={"class":"rating_nums"}).get_text().strip()
        buy_info=book_info.find(attrs={"class":"buy-info"}).get_text().strip()
        pl=book_info.find(attrs={"class":"pl"}).get_text().strip()
        name=book_info.h2.get_text().strip()
        book={}
        book['name']=name
        book['pl']=pl
        book['buy_info']=buy_info
        book['rating_nums']=rating_nums
        book['pub']=pub
        book['pic']=pic

        return book



book=Book("东野圭吾")
book_info=book.detail()
print(book_info)
