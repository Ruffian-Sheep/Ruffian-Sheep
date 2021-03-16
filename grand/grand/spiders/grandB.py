import scrapy
from grand.items import GrandItem
import requests
import random
import os
from fake_useragent import UserAgent


class GrandbSpider(scrapy.Spider):
    name = 'grandB'
    allowed_domains = ['http://m.90mh.com']
    start_urls = ['http://m.90mh.com/manhua/GrandBlue/']
    file_path = r"C:\Users\ruffian\Desktop\scr\grand\img"

    def parse(self, response):
        divs = response.xpath('//div[@class="list"]/ul/li/a')
        if not divs:
            self.log("list page error--%s" % response.url)
        for div in divs:
            item = GrandItem()
            item['name'] = div.xpath('span/text()')[0].extract()
            item['name_url'] = div.xpath('@href')[0].extract()
            yield scrapy.Request(url=item['name_url'], meta={"item": item},
                                 callback=self.parse_detail, dont_filter=True)

# 接收上个函数的返回值，进行解析
    def parse_detail(self, response):
        count = int(response.xpath('//*[@id="k_total"]/text()')[0].extract())
        item = response.meta['item']
        for num in range(count):
            html_num = '-%d' % (num + 1) if num > 0 else ''

            yield scrapy.Request(url=item['name_url'].replace('.html', html_num + '.html'),
                                 meta={"item": item, 'page': num+1}, callback=self.parse_deep, dont_filter=True)

    def parse_deep(self, response):
        img_url = response.xpath('//div[@id="chapter-image"]/a/img/@src')[0].extract()
        if not img_url:
            self.log("list page error--%s" % response.url)
            yield item
        item = response.meta['item']
        item['num'] = response.meta['page']
        item['img_url'] = img_url
        yield item
