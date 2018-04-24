# -*- coding: utf-8-*-
import sys, requests,json, os, io, csv
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from mongohelp import MongoHelper
from bson import Binary, Code
from bson.json_util import dumps
from bson import json_util
from multiprocessing.dummy import Pool as ThreadPool  # 线程池
from progressbar import ProgressBar
from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
from requests import Session
class HtmlParser:
    def __init__(self,url='https://avio.pw/cn/released/',pages=range(2,298)):
        # self.session = requests.session()
        self.session = FuturesSession(executor=ProcessPoolExecutor(max_workers=16),session=Session())
        self.entry_url = url
        self.search_url = 'https://www.javbus7.com/'
        self.mongo = MongoHelper()
        self.pages = pages
        self.bar = ProgressBar(total=len(pages))

    def get_error(self):
        return self.error_ids

    def get_error_pages(self):
        return self.error_pages

    def parse(self):
        pool = ThreadPool(16)  # 创建一个线程池，16个线程数
        pool.map(self.parse_page, self.pages)  # 将任务交给线程池，所有url都完成后再继续执行，与python的map方法类似
        pool.close()
        pool.join()

    def parse_page(self,page):
        try:
            resp = self.get_html(self.entry_url+"page/"+str(page))
            html = BeautifulSoup(resp,'html.parser')
            div_bricks = html.find('div',id="waterfall")
            if div_bricks is None:
                # print("!!!分析第"+str(page)+"页出错!!!")
                self.error_pages.append(page)
                self.bar.move()
                self.bar.log('{0:0>4}'.format(page))
                return
            bricks = div_bricks.find_all('a')
            count = len(bricks)
            # print("第"+str(page)+"页")
            for item in bricks:
                ID = item.find_all("date")[0].string
                Title = item.find_all("img")[0]['title']
                Date = item.find_all("date")[1].string
                URL = item['href']
                av = self.mongo.get_one_by('_id',ID)
                if av is None:
                    self.parse_item(ID=ID,Title=Title,URL=URL)
        except TypeError:
            self.error_pages.append(page)
        self.bar.move()
        self.bar.log('{0:0>4}'.format(page))

    def parse_item(self,ID,Title,URL):
        data ={}
        genre = {}
        star = {}
        data["_id"] = ID
        data["URL"] = URL
        data["Title"] = Title
        data["Studio"] = ""
        data["StudioLink"] = ""
        data["Label"] = ""
        data["LabelLink"] = ""
        data["Director"] = ""
        data["DirectorLink"] = ""
        data["Series"] = ""
        data["SeriesLink"] = ""
        data["Cover"] = ""
        data["Genres"] = {}
        data["Stars"] = {}
        data["Samples"] = []
        resp = self.get_html(URL)
        html = BeautifulSoup(resp,'html.parser')
        info = html.find('div',"col-md-3 info")
        # print(info)
        if info is None:
            # print('First at '+ID)
            resp = self.get_html(self.search_url+ID)
            html = BeautifulSoup(resp,'html.parser')
            info = html.find('div',"col-md-3 info")
            if info is None:
                self.error_ids.append(ID+" "+URL)
                return False

        data["Cover"] = html.find('a',"bigImage")['href']
        ########## Date ###########
        d = info.find_all("p")[1].text[6:]
        data["Date"] = d
        # print("date: "+d)
        ######### Length###########
        l = info.find_all("p")[2].text[4:]
        data["Length"] = l
        # print("Length: "+l)
        texts = info.find_all("a")
        for text in texts:
            link = text['href']
            string = text.text
            if link.find("studio") >=0:
                data["Studio"] = string
                data["StudioLink"] = link
                # print("Studio: "+string+ " : "+link)
            if link.find("label") >=0:
                data["Label"] = string
                data["LabelLink"] = link
                # print("Label: "+string+ " : "+link)
            if link.find("director") >=0:
                data["Director"] = string
                data["DirectorLink"] = link
                # print("Director: "+string+ " : "+link)
            if link.find("series") >=0:
                data["Series"] = string
                data["SeriesLink"] = link
                # print("Series: "+string+ " : "+link)
            if link.find("genre") >=0:
                genre[string] = link
        data["Genres"] = genre

        st = html.find_all('a',"avatar-box")
        if st is not None and len(st) >0:
            for s in st:
                link = s['href']
                name = s.text.strip()
                star[name] = link
                # print("Stars: "+name+ " : "+link)
        data["Stars"] = star

        samples = html.find_all('a',"sample-box")
        if samples is not None and len(samples) >0:
            for s in samples:
                data["Samples"].append(s['href'])

        self.mongo.insert_one(data)
