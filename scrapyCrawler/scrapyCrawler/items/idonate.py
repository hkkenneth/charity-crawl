import scrapy

class IDonateBaseItem(scrapy.Item):
    LIST_KEYS = []
    source_url = scrapy.Field()
    source_id = scrapy.Field()
    source_lang = scrapy.Field()
    source_name = scrapy.Field()
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    icon = scrapy.Field()

class IDonateSummaryItem(IDonateBaseItem):
    objective = scrapy.Field()
    summary = scrapy.Field()
    detail_url = scrapy.Field()

class IDonateDetailItem(IDonateBaseItem):
    review = scrapy.Field()
    advice = scrapy.Field()
    description = scrapy.Field()
    website = scrapy.Field()
