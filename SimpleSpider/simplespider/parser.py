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
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url_et')


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

    def content_zhilian(self, response, database):
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//*[@class="summary-plane__title"]/text()').extract_first()
        salary = selector.xpath('//*[@class="summary-plane__salary"]/text()').extract_first()
        city = selector.xpath('//*[@class="summary-plane__info"]/li/a/text()').extract_first()
        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//*[@class="describtion__detail-content"]').extract()
        summary_info = selector.xpath('//*[@class="summary-plane__info"]/li/text()').extract()

        if len(summary_info) == 3:
            experience = selector.xpath('//*[@class="summary-plane__info"]/li/text()').extract()[0]
            education = selector.xpath('//*[@class="summary-plane__info"]/li/text()').extract()[1]
            data = {"title":title, "salary":salary, "city":city, "experience":experience, "education":education, "description":description}
        else:
            data = {"title":title, "salary":salary, "city":city, "summary_info":summary_info, "description":description}

        database.insert(data)

    def content_qiancheng(self, response, database):
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//div[@class="cn"]/h1/text()').extract_first()
        salary = selector.xpath('//div[@class="cn"]/strong/text()').extract_first()

        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//div[@class="bmsg job_msg inbox"]/*[not(@class)]').getall()
        summary_info = city = selector.xpath('//p[@class="msg ltype"]/@title').extract_first().split('\xa0\xa0|\xa0\xa0')

        if len(summary_info) >= 3:
            city = summary_info[0]
            experience = summary_info[1]
            education = summary_info[2]
            data = {"title":title, "salary":salary, "city":city, "experience":experience, "education":education, "description":description}
        else:
            data = {"title":title, "salary":salary, "summary_info":summary_info, "description":description}

        database.insert(data)


    def content_boss(self):
        pass
    def content_shixi(self):
        pass
    def content_lagou(self):
        pass