# -*- coding: utf-8 -*-

# Scrapy settings for scrapyCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapyCrawler'

SPIDER_MODULES = ['scrapyCrawler.spiders']
NEWSPIDER_MODULE = 'scrapyCrawler.spiders'

ITEM_PIPELINES = {
    'scrapyCrawler.pipelines.ListExtractionPipeline': 50,
    'scrapyCrawler.pipelines.NamePipeline': 300,
    'scrapyCrawler.pipelines.SeenNamePipeline': 600,
    'scrapyCrawler.pipelines.TelephoneSanitizePipeline' : 700,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyCrawler (+http://www.yourdomain.com)'
