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
    def __init__(self):
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url')

        #self.selector = Selector()

    def list_zhilian(self, response_text):
        urls = []
        page = json.loads(response_text)

        if not len(page['data']['results']):
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

    def content_zhilian(self, response, database):
        pp = Selector(response)
        title = pp.xpath('//*[@class="summary-plane__title"]/text()').extract_first()
        salary = pp.xpath('//*[@class="summary-plane__salary"]/text()').extract_first()
        city = pp.xpath('//*[@class="summary-plane__info"]/li/a/text()').extract_first()
        description = pp.xpath('//*[@class="describtion__detail-content"]').extract()
        #description = ''.join(description).replace("<p>", "").replace("<br>", "").replace("<b>", "").replace("</b>", "").replace("</p>", "\n")
        summary_info = pp.xpath('//*[@class="summary-plane__info"]/li/text()').extract()

        if len(summary_info) == 3:
            experience = pp.xpath('//*[@class="summary-plane__info"]/li/text()').extract()[0]
            education = pp.xpath('//*[@class="summary-plane__info"]/li/text()').extract()[1]
            data = {"title":title, "salary":salary, "city":city, "experience":experience, "education":education, "description":description}
        else:
            data = {"title":title, "salary":salary, "city":city, "summary_info":summary_info, "description":description}

        database.insert(data)

    def content_qiancheng(self):
        pass
    def content_boss(self):
        pass
    def content_shixi(self):
        pass
    def content_lagou(self):
        pass