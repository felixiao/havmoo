# -*- coding: utf-8-*-
import sys, requests,json, os, io, csv
from datetime import datetime
from mongohelp import MongoHelper
from bson import Binary, Code
from bson.json_util import dumps
from bson import json_util

class DataHandler:
    # 增删改查mongodb
    # 保存到文件
    def __init__(self):
        self.mongo=MongoHelper()

    def AddData(self,data):
        self.mongo.insert_one(data)

    def AddError(self,error):
        self.mongo.insert_one(error):

    def SaveFiles(self):
        datas = []
        datacsv = []
        for av in self.mongo.get_collection():
            data ={}
            datac=[]
            data["_id"] = av["_id"]
            data["Date"] = av["Date"]
            data["Title"] = av["Title"]
            data["URL"] = av["URL"]
            data["Length"] = av["Length"]
            data["Studio"] = av["Studio"]
            data["StudioLink"] = av["StudioLink"]
            data["Label"] = av["Label"]
            data["LabelLink"] = av["LabelLink"]
            data["Director"] = av["Director"]
            data["DirectorLink"] = av["DirectorLink"]
            data["Series"] = av["Series"]
            data["SeriesLink"] = av["SeriesLink"]
            data["Genres"] = av["Genres"]
            data["Stars"] = av["Stars"]
            data["Cover"] = av["Cover"]
            data["Samples"] = av["Samples"]
            datac.append(av["_id"])
            datac.append(av["Date"])
            datac.append(av["Title"])
            datac.append(av["URL"])
            datac.append(av["Length"])
            datac.append(av["Studio"])
            datac.append(av["StudioLink"])
            datac.append(av["Label"])
            datac.append(av["LabelLink"])
            datac.append(av["Director"])
            datac.append(av["DirectorLink"])
            datac.append(av["Series"])
            datac.append(av["SeriesLink"])
            datac.append(av["Genres"])
            datac.append(av["Stars"])
            datac.append(av["Cover"])
            datac.append(av["Samples"])
            datacsv.append(datac)
            datas.append(data)

        sys.stdout.write(' ' * 79 + '\r')
        sys.stdout.write('saved  '+str(len(datacsv))+' avs! parsed '+str(len(parser.pages)-len(parser.get_error_pages()))+'/'+str(len(parser.pages))+'\n')

        seconds = (datetime.utcnow() - datetime(1, 1, 1)).total_seconds()
        with open('./data/avs'+str(seconds)+'.csv', 'w', encoding='utf8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['_id', 'Date', 'Title','URL', 'Length', 'Studio', 'StudioLink', 'Label', 'LabelLink', 'Director', 'DirectorLink','Series','SeriesLink','Genres','Stars','Cover','Samples'])
            spamwriter.writerows(datacsv)
        with io.open('./data/avs'+str(seconds)+'.json', 'w', encoding='utf8') as outfile:
            data = json.dumps(datas, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write(data)
            outfile.close()
        with io.open('./data/error'+str(seconds)+'.txt', 'w', encoding='utf8') as outfile:
            data = json.dumps(parser.get_error(), sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write(data)
            outfile.close()
        with io.open('./data/error_page.txt', 'w', encoding='utf8') as outfile:
            data = json.dumps(parser.get_error_pages(), sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write(data)
            outfile.close()
