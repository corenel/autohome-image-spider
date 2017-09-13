# -*- coding: utf-8 -*-
"""Item pipelines."""

import csv
import os
import shutil
import time

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

import misc.config as cfg
from misc.utils import save_dict


class ImageCrawlPipeline(object):
    """Pipeline for crawling car images."""

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


class DataWritePipeline(object):
    """Pipeline for saving car image items into csv file."""

    def __init__(self):
        """Init DataWritePipeline."""
        self.item_writer = None
        self.brand_name_dict = {}
        self.fct_name_dict = {}
        self.series_name_dict = {}
        self.spec_name_dict = {}
        if not os.path.isdir(cfg.csv_root):
            os.makedirs(cfg.csv_root)
        self.time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.item_fn = os.path.join(cfg.csv_root,
                                    "{}_item.csv".format(self.time))
        self.dict_fn = os.path.join(cfg.csv_root,
                                    "{}_dict.csv".format(self.time))
        self.dict_path = os.path.join(cfg.csv_root,
                                      "{}".format(self.time) + "_{}.pkl")

    def process_item(self, item, spider):
        """Process item."""
        if self.item_writer is None:
            self.item_writer = csv.writer(open(self.item_fn, 'a'))
        self.item_writer.writerow([item["brand_id"],
                                   item["fct_id"],
                                   item["series_id"],
                                   item["spec_id"],
                                   item["image_type"],
                                   item["image_id"],
                                   item["image_url"]])

        save_dict(self.brand_name_dict, spider.brand_name_dict,
                  self.dict_path.format("brand_name_dict"))
        save_dict(self.fct_name_dict, spider.fct_name_dict,
                  self.dict_path.format("fct_name_dict"))
        save_dict(self.series_name_dict, spider.series_name_dict,
                  self.dict_path.format("series_name_dict"))
        save_dict(self.spec_name_dict, spider.spec_name_dict,
                  self.dict_path.format("spec_name_dict"))

        self.brand_name_dict = spider.brand_name_dict
        self.fct_name_dict = spider.fct_name_dict
        self.series_name_dict = spider.series_name_dict
        self.spec_name_dict = spider.spec_name_dict

        return item


class ImagesDownloadPipeline(ImagesPipeline):
    """Pipeline for downloading car images."""

    def file_path(self, request, response=None, info=None):
        """Return file path for images."""
        image_guid = request.url.split('/')[-1]
        return '%s' % (image_guid)

    def get_media_requests(self, item, info):
        """Return image url request."""
        yield scrapy.Request(item["image_url"])

    def item_completed(self, results, item, info):
        """Post process when downloaded."""
        image_paths = [x['path'] for ok, x in results if ok]
        image_raw_path = os.path.join(cfg.image_raw_root, image_paths[0])
        image_ext = os.path.splitext(image_raw_path)[1]
        image_path = os.path.join(cfg.image_root,
                                  str(item["brand_id"]),
                                  str(item["fct_id"]),
                                  str(item["series_id"]),
                                  str(item["spec_id"]),
                                  str(item["image_type"]),
                                  "{}{}".format(item["image_id"], image_ext))

        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))

        if not image_paths:
            raise DropItem("Item contains no images")

        if os.path.exists(image_raw_path) and not os.path.exists(image_path):
            shutil.move(image_raw_path, image_path)
            print("download {}-{}-{}-{}-{}-{} to {}".format(
                item["brand_id"],
                item["fct_id"],
                item["series_id"],
                item["spec_id"],
                item["image_type"],
                item["image_id"],
                image_path))

        item['image_path'] = image_path
        return item
