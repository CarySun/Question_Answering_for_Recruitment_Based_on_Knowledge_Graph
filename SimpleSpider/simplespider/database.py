#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16 

import pymongo


class MongoDB():

    def __init__(self, database, keyword):
        """
        初始化

        :param database: 不同的网站用不同db
        :param keyword:  不同职位构成不同的表
        """
        self.conn = pymongo.MongoClient()
        self.db = self.conn[database]
        self.col = self.db[keyword]

    def insert(self, data):

        # if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
        #     print('代理不符合规范', proxy, '丢弃')
        #     return
        # if not self.db.zscore(REDIS_KEY, proxy):
        #     return self.db.zadd(REDIS_KEY, {proxy:score})
        # todo 验证职位是否重复?
        self.col.insert_one(data)

    def delete(self, data):
        pass

    def seek(self, key_dict):
        pass

    def count(self):
        pass


if __name__ == '__main__':
    text = {'name': 'cary', 'age': 25}
    mongo = MongoDB('test_mongo', 'work')
    mongo.insert(text)


