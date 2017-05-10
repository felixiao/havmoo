# -*- coding: utf-8-*-
import sys, requests, json, os, datetime, time, eyed3
from pymongo import MongoClient

class MongoHelper:
    def __init__(self):
        self.client = MongoClient()# MongoClient是线程安全的且内部维护了一个连接池，所以全局使用一个即可
        self.db = self.client['javbus']
        self.folder = './bus/'
    def get_db(self):
        return self.db

    def get_table(self):
        return self.db['av']

    def get_collection(self):
        collection = self.db['av'].find()
        return collection

    def insert_one(self,data):
        avs = self.db['av']
        data['updateTime'] = str(datetime.datetime.utcnow())  # 我们最好记录下更新的时间
        av = avs.find_one({'_id':data['_id']})
        if av is None:
            av = avs.insert(data)
            print("ID = "+data['_id'])

    def insert_multi(self,data):
        for av in data:
            self.insert_one(av)

    # 去除标题中的非法字符 (Windows)
    def validate_title(self,title):
        invalid_characaters = '\\/:*?"<>|.'
        new_title = title
        for c in invalid_characaters:
            #print 'c:', c
            new_title = new_title.replace(c, '_')
        new_title = new_title.strip(' ')
        return new_title

    def get_one_by(self,key,value):
        results = self.db['av'].find({key:value})
        return results

    def update_one_by_id(self,data):
        song = self.db['av'].update_one(
            filter={'_id': data['sid']+'a'+data['aid']+'s'+data['ssid']},
            update={'$set': data},
            upsert=True
        )
        print(av)
        return av

    def delete_one_by_id(self,id):
        av = self.db['av'].remove({'_id':id})
        print(av['title']+" deleted!")

    def clear(self):
        self.db['av'].remove({})

    def read(self,avs):
        self.insert_multi(avs)
