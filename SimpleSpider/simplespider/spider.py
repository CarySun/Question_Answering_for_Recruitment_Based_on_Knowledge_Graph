#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16
from io import BytesIO
import time

import redis
import requests

from bloom_filter import BloomFilter
from database import MongoDB
from parser import WebParser
import get_proxy


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.140 Safari/537.36 '
}

keywords = ['机器学习', '数据挖掘', '知识图谱', '推荐系统', '深度学习', '算法工程师', '前端', '后端', 'Java', 'Python', '产品经理', '数字产品经理']



# 城市编号 {北京: 530, 深圳: 765, 上海: 538, 广州: 763, 成都: 801, 西安: 854}




class JobSpider(object):
    def __init__(self, keywords_dict, redis_key):
        #self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url')
        self.parser = WebParser(redis_key)
        self.keywords = keywords_dict

    def crawl_zhilian(self, city, keyword):
        #url_list = []  # todo url_list 做成堆栈形式
        begin_url = 'https://fe-api.zhaopin.com/c/i/sou?start={page}&pageSize=90&cityId={city}&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={keyword}&kt=3'
        database = MongoDB('zhilian', self.keywords[keyword])

        url_list = self._get_list(begin_url, city, keyword, page_weight=90)

        print(keyword , city ,'list parser done!')
        print(len(url_list))

        self._get_content(database, url_list)

    def crawl_qiancheng(self, city, keyword):
        begin_url ='https://search.51job.com/list/{city},000000,0000,00,9,99,{keyword},2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
        database = MongoDB('qiancheng', self.keywords[keyword])

        url_list = self._get_list(begin_url, city, keyword, page_begin=1, web_name='qiancheng')

        print(keyword, city, 'list parser done!')
        if url_list:
            print(len(url_list))

        self._get_content(database, url_list, web_name='qiancheng')

    def crawl_leipin(self, city, keyword):
        begin_url = "https://www.liepin.com/city-{city}/zhaopin/pn{page}/?d_pageSize=40&jobKind=2&key={keyword}"
        database = MongoDB('leipin', self.keywords[keyword])

        url_list = self._get_list(begin_url, city, keyword, page_begin=0, web_name='leipin')

        print(keyword, city, 'list parser done!')
        if url_list:
            print(len(url_list))

        self._get_content(database, url_list, web_name='leipin')

    def crawl_boss(self):
        pass

    def crawl_shixi(self):
        pass

    def crawl_lagou(self):
        pass

    def _anti_progrosse(self):
        # todo 反爬虫代理函数
        proxy = get_proxy.get_proxy()
        if not proxy:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
            }
            response = requests.get(begin_url.format(page*90, city, keyword), headers=headers, proxies=proxies)
            if response.status_code != 200:
                print('proxy mode fail!!! please wait a few time, and try again')
                return
            urls = self.parser.list_zhilian(response.text)
        else:
            print("Can't seek useful proxy!")
            return

    def _get_content(self, database, url_list, web_name=None):
        # todo 此处改为多线程
        if url_list:
            for url in url_list:
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code != 200:
                        print('anti-spider in content: ', response.status_code)
                        print('error url:', url)
                        # todo 反爬虫代理函数
                        time.sleep(3)
                        response = requests.get(url, headers=headers)
                        if response.status_code != 200:
                            print('give up:', url)
                        else:
                            if web_name == 'zhilian':
                                self.parser.content_zhilian(response, database, url)
                            if web_name == 'qiancheng':
                                self.parser.content_qiancheng(response, database, url)
                            if web_name == 'leipin':
                                self.parser.content_liepin(response, database, url)
                        continue
                    if web_name == 'zhilian':
                        self.parser.content_zhilian(response, database, url)
                    if web_name == 'qiancheng':
                        self.parser.content_qiancheng(response, database, url)
                    if web_name == 'leipin':
                        self.parser.content_liepin(response, database, url)
                except Exception as e:
                    print('request_job_contain error : {}'.format(e))

    def _get_list(self, begin_url, city, keyword, page_weight=1, page_begin=0, web_name=None):
        url_list = []
        for page in range(1000):
            try:
                u = begin_url.format(page=page * page_weight + page_begin, city=city, keyword=keyword)
                response = requests.get(begin_url.format(page=page * page_weight + page_begin, city=city, keyword=keyword), headers=headers)
                if response.status_code != 200:
                    print('anti-spider in list')
                    continue  # 如果用下面的话,记得去掉这个return
                    """
                    # # todo 反爬虫代理函数
                    # proxy = get_proxy.get_proxy()
                    # if not proxy:
                    #     proxies = {
                    #         'http': 'http://' + proxy,
                    #         'https': 'https://' + proxy,
                    #     }
                    #     response = requests.get(begin_url.format(page*90, city, keyword), headers=headers, proxies=proxies)
                    #     if response.status_code != 200:
                    #         print('proxy mode fail!!! please wait a few time, and try again')
                    #         return
                    #     urls = self.parser.list_zhilian(response.text)
                    # else:
                    #     print("Can't seek useful proxy!")
                    #     return
                    """
                else:
                    if web_name == 'zhilian':
                        urls = self.parser.list_zhilian(response)
                    if web_name == 'qiancheng':
                        urls = self.parser.list_qiancheng(response)
                    if web_name == 'leipin':
                        urls = self.parser.list_liepin(response)

                if urls == (None or []):
                    break
                url_list.extend(urls)

            except Exception as e:
                print('request_job_list error : {}'.format(e))
        return url_list



if __name__ == '__main__':

    #cities = {'北京': '530', '深圳': '765', '上海': '538', '广州': '763', '成都': '801', '西安': '854', '重庆': '551', '杭州': '653'}

    #cities = {'北京': '010000', '深圳': '040000', '上海': '020000', '广州': '030200', '成都': '090200', '西安': '200200',
    #         '重庆': '060000', '杭州': '080200'}

    cities = {'北京': 'bj', '深圳': 'sz', '上海': 'sh', '广州': 'gz', '成都': 'cd', '西安': 'xian',
             '重庆': 'cq', '杭州': 'hz'}

    keywords_dict = {'机器学习': 'machine_learning', '数据挖掘': 'data_mining', '知识图谱': 'knowledge_graph', '推荐系统': 'recommended_system',
     '深度学习': 'deep_learninig', '算法工程师': 'algorithm_engineer', '前端': 'front_end', '后端': 'rear_end', 'Java': 'java',
     'Python': 'python', '产品经理': 'product_manager', '数字产品经理': 'digital_product_manager'}

    test = JobSpider(keywords_dict, 'kl')

    for keyword in keywords:

        for city in cities.values():
            test.crawl_leipin(city, keyword)

        print(keyword, ' done!')
        time.sleep(60)