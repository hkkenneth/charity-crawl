import scrapy

class WiseGivingItem(scrapy.Item):
    LIST_KEYS = ['orgmemberships', 'statutorystatus']
    name = scrapy.Field()
    icon = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    yearofest = scrapy.Field()
    orghead = scrapy.Field()
    orgmemberships = scrapy.Field()
    statutorystatus = scrapy.Field()
    taxstatus = scrapy.Field()
