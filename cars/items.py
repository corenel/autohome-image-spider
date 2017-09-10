# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarsItem(scrapy.Item):
    """Cars item."""

    # info
    brand_id = scrapy.Field()
    fct_id = scrapy.Field()
    series_id = scrapy.Field()
    spec_id = scrapy.Field()
    image_url = scrapy.Field()
    color = scrapy.Field()
    inner_color = scrapy.Field()
    # image
    image_id = scrapy.Field()
    is_first_img = scrapy.Field()
    is_last_img = scrapy.Field()
    spec_is_stop = scrapy.Field()
