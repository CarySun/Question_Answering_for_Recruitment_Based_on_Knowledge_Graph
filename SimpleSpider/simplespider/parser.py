#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16
"""
作为文字解析以及最终录入数据库的工作
"""
import json
import re

from scrapy.selector import Selector
# from selenium import webdriver
from database import MongoDB
from bloom_filter import BloomFilter

class WebParser(object):
    def __init__(self):
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url')
        #self.selector = Selector()

    def list_zhilian(self, response):
        urls = []
        page = json.loads(response.text)

        if len(page['data']['results']):
            return None

        for info in page['data']['results']:
            url = info.get('positionURL')
            if not self.bloom_filter.exists(url):
                self.bloom_filter.insert(url)
                urls.append(url)
        return urls


    def list_qiancheng(self):
        pass

    def list_boss(self):
        pass

    def list_shixi(self):
        pass

    def list_lagou(self):
        pass

    def content_zhilian(self, response):
        Selector(response)

    def content_qiancheng(self):
        pass
    def content_boss(self):
        pass
    def content_shixi(self):
        pass
    def content_lagou(self):
        pass