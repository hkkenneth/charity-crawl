# -*- coding: utf-8 -*-
import scrapy
import time

from scrapyCrawler.items.idonate import IDonateSummaryItem
from scrapyCrawler.items.idonate import IDonateDetailItem

class IdonateSpider(scrapy.Spider):
    name = "idonate"
    allowed_domains = ["http://www.theidonate.com/", "localhost"]
    start_urls = (
    )
    # langs = [""]
    langs = ["en/"]

    def parse(self, response):
        url = response.url
        tokens = url.split('/')
        url = url.replace('localhost:6081', 'www.theidonate.com')

        item = IDonateDetailItem()

        item['source_url'] = url.replace('localhost:6081', 'www.theidonate.com')
        item['source_id'] = url.split('/')[-1]
        if len(self.langs[0]) == 0:
            item['source_lang'] = 'tc'
        else:
            item['source_lang'] = self.langs[0][:-1]
        item['source_name'] = self.name
        item['crawl_time'] = int(time.time())
        item['name'] = response.xpath('//header[@class="frame-top"]/h1/span/text()').extract()
        item['icon'] = ['http://www.theidonate.com' + src for src in response.xpath('//header[@class="frame-top"]/h1/img[@class="charity-logo"]/@src').extract()]
        item['review'] = response.xpath('//p[@class="review"]/text()').extract()
        item['advice'] = response.xpath('//p[@class="advice"]/text()').extract()
        item['description'] = response.xpath('//p[@class="description"]/text()').extract()
        item['website'] = response.xpath('//p[@class="home"]/a/@href').extract()
        return item

    def parse_index(self, response):
        url = response.url
        url = url.replace('localhost:6081', 'www.theidonate.com')
        summary_divs = response.xpath('//div[@class="charity-summary"]')
        requests = []
        for index, summary_div in enumerate(summary_divs):
            item = IDonateSummaryItem()
            item['source_url'] = url
            item['source_id'] = None
            if len(self.langs[0]) == 0:
                item['source_lang'] = 'tc'
            else:
                item['source_lang'] = self.langs[0][:-1]
            item['source_name'] = self.name
            item['crawl_time'] = int(time.time())
            item['name'] = summary_div.xpath('div[@class="text-info"]/h3/a[1]/span/text()').extract()
            item['icon'] = ['http://www.theidonate.com' + src for src in summary_div.xpath('div[@class="text-info"]/h3/a[1]/img[@class="charity-logo"]/@src').extract()]
            item['objective'] = summary_div.xpath('div[@class="text-info"]/p[@class="objective"]/text()').extract()
            item['summary'] = summary_div.xpath('div[@class="text-info"]/p[@class="summary"]/text()').extract()
            item['detail_url'] = summary_div.xpath('div[@class="text-info"]/h3/a[1]/@href').extract()
            detail_url = None
            if len(item['detail_url']) == 1:
                tokens = item['detail_url'][0].split('/')
                item['source_id'] = tokens[-1]
                detail_url = item['detail_url'][0].replace('http://', '').replace('www.theidonate.com', '')
                requests.append(scrapy.Request('http://localhost:6081' + detail_url, callback=self.parse))
            yield item
        for req in requests:
            yield req


    def start_requests(self):
        for page in range(1, 23):
            for lang in self.langs:
                url = "http://localhost:6081/" + lang + "ranking?sort=rank&q=+&rank=&demand=&page=" + str(page)
                yield scrapy.Request(url, self.parse_index)  # is there a way to pass info here so the parse know the value of id, lang and page?
