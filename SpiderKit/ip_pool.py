import requests
from bs4 import BeautifulSoup
import random
from SpiderKit.agents import agents


"""
    ip代理池
    实现的功能：
    1、 爬取ip代理网站的ip地址 约10~20页
    2、 利用计时器定期更新ip地址
    3、 由于程序的架构，此类对象的调用会写在spider类中，MyResquest将接受它的对象
    
    4、 不同的ip提供方式，随机选择和ip轮询等等
"""

url = 'http://www.xicidaili.com/nn/{page}'


class IPProvider:
    def __init__(self, numopages=5):
        self.__numopages = numopages
        self.__ip_list = []
        self.__count = 0

    def __get_ip_list(self, ):
        # 提取页面源码
        # 每一页

        for i in range(1, 1+self.__numopages):
            headers = {'User-Agent': random.choice(agents)}
            r = requests.get(url=url.format(page=i), headers=headers)
            r.encoding = 'utf-8'

            # 关键区域抽取
            soup = BeautifulSoup(r.text, 'lxml')
            trs = soup.find_all('tr')
            for j in range(1, len(trs)):
                tr = trs[j]
                items = tr.find_all('td')
                ip = 'http://' + items[1].text + ':' + items[2].text
                self.__ip_list.append(ip)

    def getIP(self, random_mod=False):
        if len(self.__ip_list) < 1:
            self.__get_ip_list()
        self.__count += 1
        return random.choice(self.__ip_list) if random_mod else self.__ip_list[self.__count % len(self.__ip_list)]

    def getIPlist(self):
        if len(self.__ip_list) < 1:
            self.__get_ip_list()
        return self.__ip_list


if __name__ == '__main__':
    ip = IPProvider(1)
    print(ip.getIP())
    print(ip.getIP())
    print(ip.getIP())


