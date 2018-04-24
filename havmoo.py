# -*- coding: utf-8-*-
import sys, requests,json, os, io
from parser import HtmlParser
from datahandler import DataHandler
if __name__ == '__main__':
    parse = HtmlParser()

    datahandler = DataHandler()
    datahandler.SaveFiles()
    # 判断要检索的范围

    downList=[]
    with open('./data/error_page.txt') as data_file:
        downList = json.load(data_file)

    parser = HtmlParser()
    parser.pages = downList
    parser.bar = ProgressBar(total=len(downList))
    parser.parse()
