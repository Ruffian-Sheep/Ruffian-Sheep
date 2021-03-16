import scrapy
from ips.items import IpsItem
import requests
from fake_useragent import UserAgent

class IpsSpider(scrapy.Spider):
    name = 'IPS'
    allowed_domains = ['www.xiladaili.com']
    page_num=5
    start_urls = ['http://www.xiladaili.com/gaoni/'] 

    def parse(self, response):
        self.log('=====================',response.text)
        item = IpsItem()
        divs = response.xpath('//div[@class="fl-table"]//tr')
        if not divs:
            self.log("list page error--%s" % response.url)
        for div in divs:
            item['ip'] = div.xpath('td[0]/text()')
            #item['port'] = div.xpath('td[1]/text()')
            item['mtd'] = div.xpath('td[1]/text()').rstrip('代理').lower().split(',')
            result=requests.get('http://www.baidu.com',proxies={item['mtd'][0]: item['ip']},headers={'User-Agent', UserAgent().random},timeout=15)
            if result.status_code == 200 :

                yield item
    
