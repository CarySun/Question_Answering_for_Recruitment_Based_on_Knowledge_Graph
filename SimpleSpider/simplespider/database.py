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





