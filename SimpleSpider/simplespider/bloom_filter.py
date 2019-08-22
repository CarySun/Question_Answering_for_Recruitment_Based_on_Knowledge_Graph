#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author : CarySun
# @Date : 2019/8/16

import redis

# 设置散列函数的个数
BLOOMFILTER_HASH_NUMBER = 6
# # 布隆过滤器设置bit参数，默认30，占用128M空间，去重量在1亿左右
# 此参数决定了位数组的位数，如果BLOOMFILTER_BIT为30，则位数组
# 位2的30次方，这将暂用Redis
# 128MB的存储空间，url去重数量在1亿左右，
# 如果爬取的量在10亿，20
# 亿或则更高，则需要将此参数调高
BLOOMFILTER_BIT = 30


class HashMap(object):
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed

    def hash(self, value):
        """
        Hash Algorithm
        :param value: Value
        :return: Hash Value
        """
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.m - 1) & ret


class BloomFilter(object):
    def __init__(self, server, key, bit=BLOOMFILTER_BIT, hash_number=BLOOMFILTER_HASH_NUMBER):
        """
        Initialize BloomFilter
        :param server: Redis Server
        :param key: BloomFilter Key
        :param bit: m = 2 ^ bit
        :param hash_number: the number of hash function
        """
        # default to 1 << 30 = 10,7374,1824 = 2^30 = 128MB, max filter 2^30/hash_number = 1,7895,6970 fingerprints
        self.m = 1 << bit
        self.seeds = range(hash_number)
        self.server = server
        self.key = key
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]

    def exists(self, value):
        """
        if value exists
        :param value:
        :return:
        """
        if not value:
            return False
        exist = True
        for _map in self.maps:
            offset = _map.hash(value)
            exist = exist & self.server.getbit(self.key, offset)
        return exist == 1

    def insert(self, value):
        """
        add value to bloom
        :param value:
        :return:
        """
        for f in self.maps:
            offset = f.hash(value)
            self.server.setbit(self.key, offset, 1)


if __name__ == '__main__':
    # 用法127.0.0.1:6379
    client = redis.StrictRedis(host='localhost', port=6379)
    bl = BloomFilter(client, 'bl:url')
    url = 'http://www.wanfangdata.com.cn/details/detaype=conference&id=7363410'
    bl.insert(url)
    result = bl.exists(url)
    print(result)
    url1 = 'http://www.wanfangdata.com.cn/details/detaype=conference&id=73634101'
    result = bl.exists(url1)
    print(result)

    if not bl.exists(url):
        bl.insert(url)
        # 同时进行爬虫操作