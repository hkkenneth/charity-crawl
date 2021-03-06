import scrapy

class WiseGivingBaseItem(scrapy.Item):
    LIST_KEYS = ['orgmemberships', 'statutorystatus', 'professionalbody', 'mission', 'objectives', 'services', 'achievements', 'report']
    source_url = scrapy.Field()
    source_id = scrapy.Field()
    source_lang = scrapy.Field()
    source_name = scrapy.Field()
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    icon = scrapy.Field()

class WiseGivingItem(WiseGivingBaseItem):
    telephone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    yearofest = scrapy.Field()
    orghead = scrapy.Field()
    orgmemberships = scrapy.Field()
    religious = scrapy.Field()
    political = scrapy.Field()
    internationalbody = scrapy.Field()
    professionalbody = scrapy.Field()
    statutorystatus = scrapy.Field()
    taxstatus = scrapy.Field()

class WiseGivingReportItem(WiseGivingBaseItem):
    mission = scrapy.Field() 
    objectives = scrapy.Field() 
    services = scrapy.Field() 
    achievements = scrapy.Field() 
    reports = scrapy.Field() 

