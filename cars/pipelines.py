# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CarsPipeline(object):
    """Pipeline for car images."""

    def process_item(self, item, spider):
        """Process item."""
        print("parsing {}-{}-{}-{}-{}: {}".format(
            item["brand_id"],
            item["fct_id"],
            item["series_id"],
            item["spec_id"],
            item["image_id"],
            item["image_url"]))
        return item
