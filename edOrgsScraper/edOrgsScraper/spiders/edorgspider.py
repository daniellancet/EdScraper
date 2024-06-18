import scrapy
from bs4 import BeautifulSoup



class OrgSpider(scrapy.Spider):
    name = "orgspider"
    allowed_domains = ["empowerillinois.org"]
    start_urls = ["https://empowerillinois.org/"]
    #custom_settings = {"RETRY_TIMES": 2, "DEPTH_LIMIT": 2}

    def parse(self, response):
        soup_str = self.get_text(response)
        yield {
            "url": response.url, 
            "soup": soup_str,
        }

        for href in response.xpath("//a/@href").getall():
            next_page = response.urljoin(href)
            if self.is_allowed_domain(next_page):
                yield scrapy.Request(next_page, self.parse)

    def is_allowed_domain(self, url):
        """ Check if the url belongs to the allowed domain """
        return any(domain in url for domain in self.allowed_domains)
    
    def get_text(self, response):
            soup = BeautifulSoup(response.body)
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            visible_text = visible_text.replace("\n", " ")
            visible_text = visible_text.replace("\t", " ")
            return visible_text
    

    def do_nothing():
         return 