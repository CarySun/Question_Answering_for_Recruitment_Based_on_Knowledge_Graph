#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16 
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

proxy_url = 'http://localhost:10200/random' # todo 最后改为配置文件


def get_proxy(test_url, proxy_url=proxy_url, max_try=3):
    max_try = max_try
    if max_try <= 0:
        return None
    max_try -= 1

    try:
        r = requests.get(proxy_url)
        proxy = BeautifulSoup(r.text, "lxml").get_text()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            response = requests.get(test_url, proxies=proxies, verify=False, timeout=(2, 5))
            if response.status_code == 200:
                return proxy
            else:
                proxy = get_proxy(test_url, proxy_url=proxy_url, max_try=max_try)
                return proxy
        except Exception:
            proxy = get_proxy(test_url, proxy_url=proxy_url, max_try=max_try)
            return proxy
    except ConnectionError:
        print("请确保代理池正常运行!!!")
        return None


if __name__ == '__main__':
    print(get_proxy('https://www.baidu.com'))