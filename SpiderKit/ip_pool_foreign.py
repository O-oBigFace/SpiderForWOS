import time
import requests
import json
import random

"""
    ip代理池
    实现的功能：
    1、 爬取ip代理网站的ip地址 约10~20页
    2、 利用计时器定期更新ip地址
    3、 由于程序的架构，此类对象的调用会写在spider类中，MyResquest将接受它的对象

    4、 不同的ip提供方式，随机选择和ip轮询等等
"""


class IPProvider:
    def __init__(self):
        self.__ip_list = []
        self.__last_time = time.time()
        self.__get_ip_list()
        self.count = 0

    def __get_ip_list(self):
        if self.count < len(self.__ip_list) and time.time() - self.__last_time < 300:
            return self.__ip_list

        # 如果里表中IP全部被弹出，或者距离上次获取IP时间间隔超过五分钟，则重新获取ip
        self.__last_time = time.time()
        self.count = 0
        r = requests.get('http://api.ip.data5u.com/api/get.shtml?order=7f21868a562a5481fc79b93bc5c01467&num=100&area=%E9%9D%9E%E4%B8%AD%E5%9B%BD&carrier=0&protocol=0&an1=1&an2=2&sp1=1&sp2=2&sort=1&system=1&distinct=0&rettype=0&seprator=%0D%0A')
        r.encoding = 'utf-8'
        rawJson = [d for d in json.loads(r.text)['data'] if d["anonymity"] == '高匿']
        self.__ip_list = rawJson
        return self.__ip_list

    def get_ip(self):
        self.__get_ip_list()
        i = self.count
        self.count += 1
        return self.__ip_list[i]



    def get_list(self):
        return self.__ip_list


if __name__ == '__main__':
    ipp = IPProvider()
    print(ipp.get_list())


