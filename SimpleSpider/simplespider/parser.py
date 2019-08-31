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
        response.encoding = response.apparent_encoding
        selector = Selector(response, type='html')
        list = selector.xpath('//div[@class="el"]/p/span/a/@href').getall()
        return urls

    def list_liepin(self, response):
        selector = Selector(response, type='html')
        list = selector.xpath('//span[@class="job-name"]/a/@href').getall()
        urls = self._filter_list(list)
        return urls

    def list_boss(self):
        pass

    def list_shixi(self):
        pass

    def list_lagou(self):
        pass

    def content_zhilian(self, response, database, url):
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//*[@class="summary-plane__title"]/text()').get()
        salary = selector.xpath('//*[@class="summary-plane__salary"]/text()').get()
        city = selector.xpath('//*[@class="summary-plane__info"]/li/a/text()').get()
        company = selector.xpath('//a[@class="company__title"]/text()').get()
        company_url = selector.xpath('//a[@class="company__title"]/@href').get()
        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//*[@class="describtion__detail-content"]').getall()
        summary_info = selector.xpath('//*[@class="summary-plane__info"]/li/text()').getall()

        if len(summary_info) == 3:
            experience = summary_info[0]
            education = summary_info[1]
            data = {'url': url, "title":title, "salary":salary, "city":city, "company":company, "company_url":company_url, "experience":experience, "education":education, "description":description}
        else:
            data = {'url': url, "title":title, "salary":salary, "city":city, "company":company, "company_url":company_url,
                    "summary_info":summary_info, "description":description}

        database.insert(data)

    def content_qiancheng(self, response, database, url):
        response.encoding = response.apparent_encoding
        selector = Selector(response)
        title = selector.xpath('//div[@class="cn"]/h1/text()').get()
        salary = selector.xpath('//div[@class="cn"]/strong/text()').get()
        company = selector.xpath('//a[@class="com_name "]/p/text()').get()
        company_url = selector.xpath('//a[@class="com_name "]/@href').get()

        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//div[@class="bmsg job_msg inbox"]').getall()
        summary_info = city = selector.xpath('//p[@class="msg ltype"]/@title').get().split('\xa0\xa0|\xa0\xa0')

        if len(summary_info) >= 3:
            city = summary_info[0]
            experience = summary_info[1]
            education = summary_info[2]
            data = {'url': url, "title":title, "salary":salary, "city":city, "company":company, "company_url":company_url, "experience":experience, "education":education, "description":description}
        else:
            data = {'url': url, "title":title, "salary":salary, "company":company, "company_url":company_url, "summary_info":summary_info, "description":description}

        database.insert(data)

    def content_liepin(self, response, database, url):
        selector = Selector(response)
        title = selector.xpath('//h1[@title]/text()').get()
        salary = selector.xpath('//p[@class="job-item-title"]/text()').get()
        if salary:
            salary = salary.strip()
        city = selector.xpath('//p[@class="basic-infor"]/span/a/text()').get()
        if city:
            city = city.split('-')[0]
        company = selector.xpath('//div[@class="company-logo"]/p/a/text()').get()
        company_url = selector.xpath('//div[@class="company-logo"]/p/a/@href').get()
        # description 结构上比较混乱,先爬取再说
        description = selector.xpath('//div[@class="job-item main-message job-description"]').getall()
        summary_info = selector.xpath('//div[@class="job-qualifications"]/span/text()').getall()

        if len(summary_info) >= 2:
            education = summary_info[0]
            experience = summary_info[1]
            data = {'url': url, "title": title, "salary": salary, "city": city, "company": company,
                    "company_url": company_url, "experience": experience, "education": education,
                    "description": description}
        else:
            data = {'url': url, "title": title, "salary": salary, "city": city, "company": company, "company_url": company_url,
                    "summary_info": summary_info, "description": description}

        database.insert(data)

    def content_boss(self):
        pass
    def content_shixi(self):
        pass
    def content_lagou(self):
        pass

    def _filter_list(self, list):
        urls = []
        for url in list:
            if not self.bloom_filter.exists(url):
                self.bloom_filter.insert(url)
                urls.append(url)
        print('done one page')
        return urls