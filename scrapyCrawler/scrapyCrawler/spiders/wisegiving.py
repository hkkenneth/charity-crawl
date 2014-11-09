# -*- coding: utf-8 -*-
import scrapy
import time

from scrapyCrawler.items.wisegiving import WiseGivingItem
from scrapyCrawler.items.wisegiving import WiseGivingReportItem

class WisegivingSpider(scrapy.Spider):
    name = "wisegiving"
    allowed_domains = ["http://www.wisegiving.org.hk/"]
    start_urls = (
    )
    langs = ["tc"] # , "tc"]
    subpages = ["page=report&"] # , "page=ngostand&", "page=finance&", "page=rules&"]
    subpage_type = 2

    def parse(self, response):
        url = response.url
        tokens = url.split('/')
        if self.subpage_type == 1:
            item = WiseGivingItem()
            item['telephone'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgtel"]/text()').extract()
            item['fax'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgfax"]/text()').extract()
            item['email'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgemail"]/text()').extract()

            item['website'] = response.xpath('//a[@id="ctl00_ContentPlaceHolder1_orgwebsite"]/@href').extract()
            item['address'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgaddress"]/text()').extract()
            item['yearofest'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgestablishyear"]/text()').extract()
            item['orghead'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_orgheadname"]/text()').extract()
            item['orgmemberships'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_membership"]/text()').extract()
            item['religious'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_religious"]/text()').extract()
            item['political'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_political"]/text()').extract()
            item['internationalbody'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_intbody"]/text()').extract()
            item['professionalbody'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_profbody"]/text()').extract()
            item['statutorystatus'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_in_statutory_status"]/text()').extract()
            item['taxstatus'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_tax_exemption_status"]/text()').extract()
        elif self.subpage_type == 2:
            item = WiseGivingReportItem()
            item['mission'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_mission"]/text()').extract()
            item['objectives'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_objective"]/text()').extract()
            item['services'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_coreservice"]/text()').extract()
            item['achievements'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_achievement"]/text()').extract()
            item['reports'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_annual_report"]/text()').extract()

        item['source_url'] = url.replace('localhost:6081', 'www.wisegiving.org.hk')
        item['source_id'] = tokens[6][(tokens[6].find('ID=') + 3):]
        item['source_lang'] = tokens[3]
        item['source_name'] = 'wisegiving'
        item['crawl_time'] = int(time.time())
        item['name'] = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_org"]/b/text()').extract()
        item['icon'] = response.xpath('//img[@id="ctl00_ContentPlaceHolder1_logo"]/@src').extract()
        return item

    def start_requests(self):
        for id in range(1, 50):
            for lang in self.langs:
                for page in self.subpages:
                    url = "http://localhost:6081/" + lang + "/donation/search/ngodetails.aspx?" + page + "ID=" + str(id)
                    yield scrapy.Request(url, self.parse)  # is there a way to pass info here so the parse know the value of id, lang and page?
