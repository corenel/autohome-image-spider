"""Spider for autohome."""

import scrapy

from misc.utils import str_to_dict


class AutohomeSpider(scrapy.Spider):
    """Spider subclass for autohome."""

    name = "autohome"

    def start_requests(self):
        """Return an iterable of Requests which spider will crawl from."""
        brand_ids = [
            33,  # 奥迪
            15,  # 宝马
            36,  # 奔驰
            44,  # 捷豹路虎
            52,  # 雷克萨斯
            70,  # 沃尔沃
            47,  # 凯迪拉克
            40,  # 保时捷
            42,  # 法拉利
            73,  # 英菲尼迪
            169,  # DS
            51,  # 林肯
            57,  # 玛莎拉蒂
            133,  # 特斯拉
            39,  # 宾利
            54,  # 劳斯莱斯
            48,  # 兰博基尼
        ]
        brand_url = "http://car.autohome.com.cn/pic/brand-{}.html"

        for brand_id in brand_ids:
            yield scrapy.Request(url=brand_url.format(brand_id),
                                 callback=self.parse)

    def parse(self, response):
        """Handle the response downloaded for each of the requests made."""
        car_model = response.xpath(
            "//script[contains(.,'__CarModel')]").re("{.*}")[0]
        filename = "car_model.log"
        with open(filename, 'a') as f:
            f.writelines("'{}'\n".format(car_model))
        self.log('Saved file %s' % filename)
