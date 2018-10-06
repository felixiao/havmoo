# -*- coding: utf-8-*-
import sys, requests, json, os, io
from bs4 import BeautifulSoup
from bson import Binary, Code
from bson.json_util import dumps
from bson import json_util
from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
from requests import Session

class HtmlParser:
    def __init__(self):
        self.session = FuturesSession(executor=ProcessPoolExecutor(max_workers=16),session=Session())
        self.search_url = 'https://www.javbus.com/'

    def parse(self,ID):
        data ={}
        genre = {}
        star = {}
        downloads = {}
        data["_id"] = ID
        data["URL"] = self.search_url+ID
        data["Title"] = ""
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
        data["Downloads"] = []
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        resp = self.session.get(self.search_url+ID,timeout=5,headers=header).result().content
        html = BeautifulSoup(resp,'html.parser')
        info = html.find('div',"col-md-3 info")
        # print(info)
        if info is None:
            if info is None:
                self.error_ids.append(ID+" "+URL)
                return False
        data["Title"] =html.find('h3').text[len(ID)+1:]
        data["Cover"] = html.find('a',"bigImage")['href']
        ########## Date ###########
        d = info.find_all("p")[1].text[6:]
        data["Date"] = d
        # print("date: "+d)
        ######### Length###########
        l = info.find_all("p")[2].text[4:-2]
        data["Length"] = int(l)
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

        datajson = {}
        with io.open('./data/'+ID+'.json', 'w', encoding='utf8') as outfile:
            datajson = json.dumps(data, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write(datajson)
            outfile.close()
        return datajson

if __name__ == '__main__':
    parser = HtmlParser()
    if len(sys.argv) > 1:
        parser.parse(sys.argv[1])
    else:
        parser.parse("IPX-001")
