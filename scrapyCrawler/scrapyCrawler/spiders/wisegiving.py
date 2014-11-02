# -*- coding: utf-8 -*-
import scrapy

from scrapyCrawler.items.wisegiving import WiseGivingItem

class WisegivingSpider(scrapy.Spider):
    name = "wisegiving"
    allowed_domains = ["http://www.wisegiving.org.hk/"]
    start_urls = (
    )
    langs = ["en"] # , "tc"]
    subpages = [""] #, "&page=report", "&page=ngostand", "&page=finance", "&page=rules"]

    def parse(self, response):
        item = WiseGivingItem()
        item['name'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_org"]/b/text()').extract()
        item['icon'] = response.xpath('//img[@id="ctl00_ContentPlaceHolder1_logo"]/@src').extract()
        item['telephone'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgtel"]/text()').extract()
        item['fax'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgfax"]/text()').extract()
        item['email'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgemail"]/text()').extract()

        item['website'] = response.xpath('//a[@id="ctl00_ContentPlaceHolder1_orgwebsite"]/@href').extract()
        item['address'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgaddress"]/text()').extract()
        item['yearofest'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgestablishyear"]/text()').extract()
        item['orghead'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgheadname"]/text()').extract()
        item['orgmemberships'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_membership"]/text()').extract()
        item['statutorystatus'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_in_statutory_status"]/text()').extract()
        item['taxstatus'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_tax_exemption_status"]/text()').extract()
        return item

    def start_requests(self):
        for id in range(1, 50):
            for lang in self.langs:
                for page in self.subpages:
                    url = "http://localhost:6081/" + lang + "/donation/search/ngodetails.aspx?ID=" + str(id) + page 
                    yield scrapy.Request(url, self.parse)  # is there a way to pass info here so the parse know the value of id, lang and page?
