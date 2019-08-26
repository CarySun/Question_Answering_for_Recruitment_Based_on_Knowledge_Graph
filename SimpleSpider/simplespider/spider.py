#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16
import redis
import requests

from bloom_filter import BloomFilter
from parser import WebParser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.140 Safari/537.36 '
}

keywords = ['机器学习', '数据挖掘', '知识图谱', '推荐系统', '深度学习', '算法工程师', '前端', '后端', 'Java', 'Python', '产品经理', '数字产品经理']

"""
https://sou.zhaopin.com/?jl=763&kw=深度学习&kt=3
jl为城市编号 {北京: 530, 深圳: 765, 上海: 538, 广州: 763, 成都: 801, 西安: 854}
kw为关键词
kt=3默认查询职位
"""


class JobSpider(object):
    def __init__(self):
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url')
        self.parser = WebParser()

    def crawl_zhilian(self, keyword):
        url_list = []
        begin_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=763&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=深度学习&kt=3'

        for page in range(100):
            response = requests.get(begin_url.format(page), headers=headers)
            urls = WebParser.list_zhilian(response)
            if urls is None:
                break
            url_list.extend(urls)

        if url_list:
            for url in url_list:
                response = requests.get(begin_url.format(page), headers=headers)
                BytesIO(response.content).read().decode()


    def crawl_qiancheng(self):
        pass

    def crawl_boss(self):
        pass

    def crawl_shixi(self):
        pass

    def crawl_lagou(self):
        pass
