import scrapy

class EdOrgs(scrapy.Item):
    def __init__(self):
        self.url = scrapy.Field()
        self.text = scrapy.Field()
        self.depth = scrapy.Field()