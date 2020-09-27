# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapWinesItem(scrapy.Item):
    wine_url = scrapy.Field()
    title = scrapy.Field()
    varietal = scrapy.Field()
    origin = scrapy.Field()
    rating = scrapy.Field()
    num_ratings = scrapy.Field()
    price = scrapy.Field()
    alc_percentage = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
