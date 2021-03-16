# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GrandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    page= scrapy.Field()
    name_url = scrapy.Field()
    img_url = scrapy.Field()
    num = scrapy.Field()
