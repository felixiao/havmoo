# -*- coding: utf-8-*-
import sys, requests,json, os,
from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
from requests import Session
class HtmlHandler:
    def __init__(self,url='https://avio.pw/cn/released/'):
        # self.session = requests.session()
        self.session = FuturesSession(executor=ProcessPoolExecutor(max_workers=16),session=Session())
        self.entry_url = url
        self.search_url = 'https://www.javbus7.com/'

    def get_html(self,url):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        prx = {'http':'http://117.90.2.178:9000',
               'http':'http://121.232.144.206:9000',
               'http':'http://121.232.145.197:9000',
               'http':'http://111.155.116.196:8123',
               'http':'http://118.117.138.29:9000'}
        try:
            # print("检索："+ID)
            return self.session.get(url,timeout=5,headers=header).result().content
        except requests.exceptions.ConnectionError:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ConnectionError @ '+url)
            return
        except requests.exceptions.ReadTimeout:
            sys.stdout.write(' ' * 79 + '\r')
            sys.stdout.write('ReadTimeout @ '+url)
            return
