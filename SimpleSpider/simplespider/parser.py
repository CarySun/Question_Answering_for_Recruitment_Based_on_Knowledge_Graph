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
import redis
# from selenium import webdriver
from database import MongoDB
from bloom_filter import BloomFilter

class WebParser(object):
    def __init__(self, redis_key):
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), redis_key)


    def list_zhilian(self, response):
        urls = []
        page = json.loads(response.text)

        if not len(page['data']['results']):
            return None

        for info in page['data']['results']:
            url = info.get('positionURL')
            if not self.bloom_filter.exists(url):
                self.bloom_filter.insert(url)
                urls.append(url)
        return urls


    def list_qiancheng(self, response):
        urls = []
        response.encoding=response.apparent_encoding
        selector = Selector(response, type='html')
        for url in selector.xpath('//div[@class="el"]/p/span/a/@href').getall():
            if not self.bloom_filter.exists(url):
                self.bloom_filter.insert(url)
                urls.append(url)
        print('done one page')
        return urls


    def list_boss(self):
        pass

    def list_shixi(self):
        pass

    def list_lagou(self):
        pass

    def content_zhilian(self, response, database, url):
        url = url
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//*[@class="summary-plane__title"]/text()').get()
        salary = selector.xpath('//*[@class="summary-plane__salary"]/text()').get()
        city = selector.xpath('//*[@class="summary-plane__info"]/li/a/text()').get()
        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//*[@class="describtion__detail-content"]').getall()
        summary_info = selector.xpath('//*[@class="summary-plane__info"]/li/text()').getall()

        if len(summary_info) == 3:
            experience = summary_info[0]
            education = summary_info[1]
            data = {'url': url, "title":title, "salary":salary, "city":city, "experience":experience, "education":education, "description":description}
        else:
            data = {'url': url, "title":title, "salary":salary, "city":city, "summary_info":summary_info, "description":description}

        database.insert(data)

    def content_qiancheng(self, response, database, url):
        url = url
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//div[@class="cn"]/h1/text()').get()
        salary = selector.xpath('//div[@class="cn"]/strong/text()').get()

        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//div[@class="bmsg job_msg inbox"]').getall()
        summary_info = city = selector.xpath('//p[@class="msg ltype"]/@title').get().split('\xa0\xa0|\xa0\xa0')

        if len(summary_info) >= 3:
            city = summary_info[0]
            experience = summary_info[1]
            education = summary_info[2]
            data = {'url': url, "title":title, "salary":salary, "city":city, "experience":experience, "education":education, "description":description}
        else:
            data = {'url': url, "title":title, "salary":salary, "summary_info":summary_info, "description":description}

        database.insert(data)


    def content_boss(self):
        pass
    def content_shixi(self):
        pass
    def content_lagou(self):
        pass