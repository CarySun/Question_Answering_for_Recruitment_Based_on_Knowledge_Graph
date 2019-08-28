#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16
from io import BytesIO

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
    def __init__(self):
        self.bloom_filter = BloomFilter(redis.StrictRedis(host='localhost', port=6379), 'job_url')
        self.parser = WebParser()
        self.keywords = {'机器学习':'machine_learning', '数据挖掘':'data_mining', '知识图谱': 'knowledge_graph', '推荐系统':'recommended_system', '深度学习':'deep_learninig', '算法工程师':'algorithm_engineer', '前端':'front_end', '后端':'rear_end', 'Java':'java', 'Python':'python', '产品经理':'product_manager', '数字产品经理':'digital_product_manager'}

    def crawl_zhilian(self, city, keyword):
        url_list = []
        begin_url = 'https://fe-api.zhaopin.com/c/i/sou?start={0}&pageSize=90&cityId={1}&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={2}&kt=3'
        database = MongoDB('zhilian', self.keywords[keyword])

        for page in range(1000):
            try:
                response = requests.get(begin_url.format(page*90, city, keyword), headers=headers)
                if response.status_code != 200:
                    print('anti-spider')
                    return # 如果用下面的话,记得去掉这个return
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
                else:
                    urls = self.parser.list_zhilian(response.text)
                if urls is None:
                    break
                url_list.extend(urls)
            except Exception as e:
                print('request_job_list error : {}'.format(e))

        if url_list:
            for url in url_list:
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code != 200:
                        print('anti-spider')
                        # todo 反爬虫代理函数
                        return
                    self.parser.content_zhilian(response, database)
                except Exception as e:
                    print('request_job_contain error : {}'.format(e))



    def crawl_qiancheng(self):
        pass

    def crawl_boss(self):
        pass

    def crawl_shixi(self):
        pass

    def crawl_lagou(self):
        pass


if __name__ == '__main__':
    test = JobSpider()
    test.crawl_zhilian(765, '机器学习')