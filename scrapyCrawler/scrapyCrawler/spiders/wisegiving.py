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
        item['name'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_org"]/b/text()').extract() or [None])[0]
        item['icon'] = (response.xpath('//img[@id="ctl00_ContentPlaceHolder1_logo"]/@src').extract() or [None])[0]
        item['telephone'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgtel"]/text()').extract() or [None])[0]
        item['fax'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgfax"]/text()').extract() or [None])[0]
        item['email'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgemail"]/text()').extract() or [None])[0]

        item['website'] = (response.xpath('//a[@id="ctl00_ContentPlaceHolder1_orgwebsite"]/@href').extract() or [None])[0]
        item['address'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgaddress"]/text()').extract() or [None])[0]
        item['yearofest'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgestablishyear"]/text()').extract() or [None])[0]
        item['orghead'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgheadname"]/text()').extract() or [None])[0]
        item['orgmemberships'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_membership"]/text()').extract()
        item['statutorystatus'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_in_statutory_status"]/text()').extract()
        item['taxstatus'] = (response.xpath('//span[@id="ctl00_ContentPlaceHolder1_tax_exemption_status"]/text()').extract() or [None])[0]
        return item

    def start_requests(self):
        for id in range(1, 6):
            for lang in self.langs:
                for page in self.subpages:
                    url = "http://www.wisegiving.org.hk/" + lang + "/donation/search/ngodetails.aspx?ID=" + str(id) + page 
                    yield scrapy.Request(url, self.parse)  # is there a way to pass info here so the parse know the value of id, lang and page?
