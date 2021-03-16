# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from grand.settings import DOWNLOAD_DIR
from fake_useragent import UserAgent
import requests
import random
import os


class GrandPipeline:
    def __init__(self):
        """
        判断下载目录是否存在
        """
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        self.ip_pool = []
        with open('C:/Users/ruffian/Desktop/ip.txt')as f:
            for i in f:
                t = i.rstrip('\n')
                self.ip_pool.append(t)
            
    def process_item(self, item, spider):
        
        if not os.path.isdir(os.path.join(DOWNLOAD_DIR, item['name'])):
            os.mkdir(os.path.join(DOWNLOAD_DIR, item['name']))
        headers = {'User-Agent': UserAgent().random}
        fail_time = 0
        while True:
            try:
                ips = random.choice(self.ip_pool)
                ip = ips[ips.index(':'):]
                if ips[:ips.index(':')] == 'http':
                    p = requests.get(item['img_url'], proxies={'http': ip}, headers=headers, timeout=10)
                else:
                    p = requests.get(item['img_url'], proxies={'https': ip}, headers=headers, timeout=10)
                with open(os.path.join(os.path.join(DOWNLOAD_DIR, item['name']), '%d.jpg' % item['num']), 'wb')as f:
                    f.write(p.content)
                return item
            except Exception as e:
                fail_time += 1
                if fail_time == 100:
                    p = '<Response [404]>'
                    raise DropItem('Fail to get ', item['name'], item['num'])
                else:
                    continue
