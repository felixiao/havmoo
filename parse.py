# -*- coding: utf-8-*-
import sys, requests,json, os, io
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from mongohelp import MongoHelper
from bson import Binary, Code
from bson.json_util import dumps
from bson import json_util

class HtmlParser:
    def __init__(self,url='https://www.javbus7.com/'):
        self.session = requests.session()
        self.entry_url = url
        self.datas = []
        self.mongo = MongoHelper()

    def parse_page(self,page):
        global bar
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        proxy = [{'http':'http://183.245.146.39:139'},
                 {'http':'http://182.88.29.70:8123'}]
        try:
            resp = self.session.get(self.entry_url,timeout=5,headers=header,proxies=proxy).content
        except requests.exceptions.ConnectionError:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ConnectionError @ '+page)
            return
        except requests.exceptions.ReadTimeout:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ReadTimeout @ '+page)
            return
        html = BeautifulSoup(resp,'html.parser')
        div_bricks = html.find_all(id="waterfall")[0].find_all('a')
        count = len(div_bricks)
        print("数量:"+str(count))
        for item in div_bricks:
            ID = item.find_all("date")[0].string
            Title = item.find_all("img")[0]['title']
            Date = item.find_all("date")[1].string
            self.parse_item(ID)
            #print(str(ID)+'_'+str(Date)+'_'+str(Title))


    def get_data(self):
        return self.datas

    def parse_item(self,ID):
        global bar
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        proxy = [{'http':'http://183.245.146.39:139'},
                 {'http':'http://182.88.29.70:8123'}]
        try:
            resp = self.session.get(self.entry_url+ID,timeout=5,headers=header,proxies=proxy).content
        except requests.exceptions.ConnectionError:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ConnectionError @ '+page)
            return
        except requests.exceptions.ReadTimeout:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ReadTimeout @ '+page)
            return
        html = BeautifulSoup(resp,'html.parser')
        Title = html.find_all("h3")[0].string
        Date = ""
        Length = ""
        Director = ""
        Studio = ""
        Label = ""
        Series = ""
        Genres = []
        Stars = []
        d = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[1].stripped_strings
        for string in d:
            Date = string
        t = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[2].stripped_strings
        for string in t:
            Length = string
        tagCount = 3
        text = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[3].text
        if text.find("導演") >= 0:
            Director = text[4:]
            tagCount += 1

        text = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[tagCount].text
        Studio = text[5:]
        tagCount += 1
        text = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[tagCount].text
        Label = text[5:]
        tagCount += 1
        text = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[tagCount].text
        if text.find("系列") >= 0:
            Series = text[4:]
            tagCount += 1
        tagCount += 1
        g = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("p")[tagCount].text.strip()
        for string in g.split("\n"):
            Genres.append(string)
        st = html.find_all(attrs={"class": "col-md-3 info"})[0].find_all("ul")
        if st is not None and len(st) >0:
            st = st[0].text.strip()
            for string in st.split("\n"):
                if string is not "":
                    Stars.append(string)

        data ={}
        data["_id"] = ID
        data["Date"] = Date
        data["Title"] = Title
        data["Length"] = Length
        data["Director"] = Director
        data["Studio"] = Studio
        data["Label"] = Label
        data["Series"] = Series
        data["Genres"] = Genres
        data["Stars"] = Stars
        self.datas.append(data)
        self.mongo.insert_one(data)

if __name__ == '__main__':
    parser = HtmlParser()
    for i in range(1,1000):
        parser.parse_page(str(i))

    with io.open('./data/avs.json', 'w', encoding='utf8') as outfile:
        data = json.dumps(parser.get_data(), sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()
