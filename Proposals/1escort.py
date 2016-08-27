import scrapy

import re
import hashlib
import time

from sam.items import SamItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

class OneEscortSpider(CrawlSpider):
    name = "1escort"
    base_url = "http://1escorts.com"
    allowed_domains = ["1escorts.com"]
    start_urls = [
        "http://1escorts.com/aldgate/",
        "http://1escorts.com/escort-kilburn/",
        "http://1escorts.com/ashford-escorts/",
        "http://1escorts.com/balham-escorts/",
        "http://1escorts.com/barbican-escorts/",
        "http://1escorts.com/barking/",
        "http://1escorts.com/bayswater-escorts/",
        "http://1escorts.com/battersea-escorts/",
        "http://1escorts.com/basildon-escorts/",
        "http://1escorts.com/barnet-escorts/",
        "http://1escorts.com/beckenham-escorts/",
        "http://1escorts.com/escort-covent-garden/",
        "http://1escorts.com/escort-ealing/",
        "http://1escorts.com/escort-finchley/",
        "http://1escorts.com/escort-finsbury/",
        "http://1escorts.com/escort-hammersmith/",
        "http://1escorts.com/escort-hampstead/",
        "http://1escorts.com/escort-harrow/",
        "http://1escorts.com/escort-hendon/",
        "http://1escorts.com/escort-high-gate/",
        "http://1escorts.com/escort-islington/",
        "http://1escorts.com/escort-kilburn/",
        "http://1escorts.com/escort-maida-vale/",
        "http://1escorts.com/escort-mill-hill/",
        "http://1escorts.com/escort-notting-hill/",
        "http://1escorts.com/escort-shepherd-bush/",
        "http://1escorts.com/escort-south-gate/",
        "http://1escorts.com/escort-st-johns-wood/",
        "http://1escorts.com/escort-swiss-cottage/",
        "http://1escorts.com/escort-watford/",
        "http://1escorts.com/escort-wembley/"
    ]

    def parse(self, response):
        alredySeen = {}
        location_raw = response.xpath('//div[@id="content"]//h1[2]/text()').extract()
        m = re.match('(.*) Escorts', location_raw[0])
        location = m.group(1).strip()
        for sel in response.xpath('//div[@id="content"]').xpath('//div[@class="lady"]'):
            item = SamItem()

            item['source']      = self.name
            item['title']       = (sel.xpath('a/text()').extract())[0]
            item['link']        = self.base_url + (sel.xpath('a/@href').extract())[0]
            item['location']    = location
            item['locationToNormalise'] = item['location']

            item['id']         = hashlib.sha224(item['link'] + self.name).hexdigest()
            if item['id'] in alredySeen:
                continue
            
            alredySeen[item['id']] = True
            item['date_published'] = int(time.time())
            detail_page_request = scrapy.Request(item['link'],
                                        callback=self.parse_detail_page, dont_filter=True)
            detail_page_request.meta['item'] = item
            yield detail_page_request

    def parse_detail_page(self, response):
        item = response.meta['item']
        sel = Selector(response)
        content = sel.xpath('//div[@id="content"]/div[1]').extract()
        detail = sel.xpath('//div[@id="content"]/p[2]/text()').extract()
        item['detail'] = detail[0]
        images_raw = sel.xpath('//div[@id="content"]/div[1]//img/@src').extract()
        images = []
        for image in images_raw:
            images.append (self.base_url + image)
        item['images'] = images
        item['price_outcall'] = item['price_incall'] = (sel.xpath('//div[@id="content"]/div[4]/ul/li[7]/text()').extract())[0]
        return item

