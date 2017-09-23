"""Spider for autohome."""

import os
import re

import scrapy

import misc.config as cfg
from cars.items import CarsItem
from misc.utils import get_car_model


class AutohomeSpider(scrapy.Spider):
    """Spider subclass for autohome."""

    name = "autohome"
    website = "http://car.autohome.com.cn"
    brand_url = "http://car.autohome.com.cn/pic/brand-{}.html"
    brand_name_dict = {}
    fct_name_dict = {}
    series_name_dict = {}
    spec_name_dict = {}
    series_to_fct_dict = {}

    def start_requests(self):
        """Return an iterable of Requests which spider will crawl from."""
        for brand_id in cfg.selected_brand_ids:
            yield scrapy.Request(url=self.brand_url.format(brand_id),
                                 callback=self.parse)

    def parse(self, response):
        """Handle the response downloaded for each of the requests made."""
        # get car model dict of brand
        car_model = get_car_model(response)
        # self.logger.info("Parsing brand {} - {}"
        #                  .format(car_model["carBrandId"],
        #                          car_model["carBrandName"]))
        brand_id = int(car_model["carBrandId"])
        self.brand_name_dict[brand_id] = car_model["carBrandName"]

        # iterate fct links
        fct_links = response.xpath(
            "//div[@class='cartab-title']/h2/a/@href").re("(.+.html)")
        if fct_links:
            for link in fct_links:
                request = scrapy.Request(
                    self.website + link, callback=self.parse_fct)
                yield request

    def parse_fct(self, response):
        """Parse factory page and get series list."""
        # get car model dict of factory
        car_model = get_car_model(response)
        # self.logger.info("--> Parsing factory {} - {}"
        #                  .format(car_model["carFctId"],
        #                          car_model["carFctName"]))
        fct_id = int(car_model["carFctId"])
        self.fct_name_dict[fct_id] = car_model["carFctName"]

        # iterate fct links
        series_links = response.xpath(
            "//span/a[contains(@href,'/pic/series/')]/@href")\
            .re("(.+.html)")
        series_t_links = ["/pic/series/{}.html"
                          .format(re.findall("\/pic\/series\/(\d+).html",
                                             s)[0]) for s in series_links]
        if series_links and series_t_links:
            for link in series_links:
                request = scrapy.Request(
                    self.website + link, callback=self.parse_series)
                yield request
            for link in series_t_links:
                request = scrapy.Request(
                    self.website + link, callback=self.parse_series)
                yield request

    def parse_series(self, response):
        """Parse series page and get spec list."""
        # get car model dict of series
        car_model = get_car_model(response)
        # self.logger.info("----> Parsing series {} - {}"
        #                  .format(car_model["carSeriesId"],
        #                          car_model["carSeriesName"]))
        fct_id = int(car_model["carFctId"])
        series_id = int(car_model["carSeriesId"])
        self.series_name_dict[series_id] = car_model["carSeriesName"]
        self.series_to_fct_dict[series_id] = fct_id

        # iterate series links
        spec_links = response.xpath(
            "//div/a[contains(@href,'/photo/series/')]/@href")\
            .re("(.+.html)")
        # just one url and it iterates all images
        # if spec_links:
        #     for link in spec_links:
        #         request = scrapy.Request(
        #             self.website + link, callback=self.parse_spec)
        #         yield request
        if spec_links:
            request = scrapy.Request(
                self.website + spec_links[0], callback=self.parse_spec)
            yield request

    def parse_spec(self, response):
        """Parse spec page and return CarsItem."""
        # get car model dict of spec
        car_model = get_car_model(response)

        # get spec info
        brand_id = int(response.xpath(
            "//div[@class='breadnav']/a[contains(@href,'/pic/brand')]/@href")
            .re('[0-9]+')[0])
        fct_id = int(self.series_to_fct_dict[car_model["CarSeriesId"]])
        series_id = int(car_model["CarSeriesId"])
        spec_id = int(car_model["CarSpec"])
        spec_name = response.xpath(
            "//div[@class='breadnav']"
            "/a[contains(@href,'/pic/series-')]/text()").extract()[0]
        color = car_model["CarColorId"]
        inner_color = car_model["CarInnerColorId"]

        # save spec dict
        if spec_id not in self.spec_name_dict:
            self.spec_name_dict[spec_id] = spec_name

        # get image info
        image_id = int(car_model["CarImgId"])
        image_type = int(car_model["CarPicTypeId"])
        is_first_img = bool(car_model["CarIsFirstPic"])
        is_last_img = bool(car_model["CarIsLastPic"])
        spec_is_stop = car_model["CarSpecIsStop"]
        image_url = "http:" + \
            response.xpath("//img[@id='img']/@src").extract()[0]
        next_url = response.xpath(
            "//script[contains(.,'nexturl')]").re("nexturl = '(.+)'")[0]

        # output
        # self.logger.info("parsing [{}][{}][{}][{}][{}]: {}".format(
        #     self.brand_name_dict[brand_id],
        #     self.fct_name_dict[fct_id],
        #     self.series_name_dict[series_id],
        #     self.spec_name_dict[spec_id],
        #     image_id,
        #     image_url))

        # add to item
        item = CarsItem()
        item["brand_id"] = brand_id
        item["fct_id"] = fct_id
        item["series_id"] = series_id
        item["spec_id"] = spec_id
        item["image_url"] = image_url
        item["color"] = color
        item["inner_color"] = inner_color
        item["image_id"] = image_id
        item["image_type"] = image_type
        item["is_first_img"] = is_first_img
        item["is_last_img"] = is_last_img
        item["spec_is_stop"] = spec_is_stop
        item_path = os.path.join(cfg.image_root,
                                 str(item["brand_id"]),
                                 str(item["fct_id"]),
                                 str(item["series_id"]),
                                 str(item["spec_id"]),
                                 str(item["image_type"]),
                                 "{}.jpg".format(item["image_id"]))
        if item["image_type"] in cfg.selected_image_types \
                and not os.path.exists(item_path):
            yield item

        # go to next image
        if not is_last_img:
            request = scrapy.Request(
                self.website + next_url, callback=self.parse_spec)
            yield request
        else:
            return
