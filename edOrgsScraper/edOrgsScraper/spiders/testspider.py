# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from bs4 import BeautifulSoup
# import pandas as pd
# import re


# class TestSpider(CrawlSpider):
#     name = "testspider"
#     allowed_domains = ["edexcelencia.org"]
#     start_urls = ["https://www.edexcelencia.org/"]

# # Define denial terms using regex for case-insensitive matching and substrings
#     deny_terms = [
#         re.escape(term) for term in [
#             r"(?i)contact",
#             r"(?i)privacy",
#             r"(?i)privacy-policy",
#             r"(?i)terms",
#             r"(?i)disclaimer",
#             r"(?i)careers",
#             r"(?i)jobs",
#             r"(?i)press",
#             r"(?i)news",
#             r"(?i)events",
#             r"(?i)blog",
#             r"(?i)donate",
#             r"(?i)volunteer",
#             r"(?i)faq",
#             r"(?i)testimonials",
#             r"(?i)sitemap",
#             r"(?i)subscribe",
#             r"(?i)advertise",
#             r"(?i)sponsors",
#             r"(?i)partners",
#             r"(?i)resources",
#             r"(?i)media",
#             r"(?i)gallery",
#             r"(?i)shop",
#             r"(?i)store",
#             r"(?i)membership",
#             r"(?i)login",
#             r"(?i)register",
#             r"(?i)signup",
#             r"(?i)support",
#             r"(?i)advertisements",
#             r"(?i)announcements",
#             r"(?i)legal",
#             r"(?i)accessibility",
#             r"(?i)feedback",
#             r"(?i)promotions",
#             r"(?i)coupons",
#             r"(?i)pricing",
#             r"(?i)products",
#             r"(?i)services",
#             r"(?i)newsletter",
#             r"(?i)social",
#             r"(?i)awards",
#             r"(?i)competitions",
#             r"(?i)investor",
#             r"(?i)webinars",
#             r"(?i)surveys",
#             r"(?i)forums",
#             r"(?i)bylaws",
#         ]
#     ]


  
#     rules = (
#         Rule(LinkExtractor(allow_domains=allowed_domains, deny = deny_terms, unique=True), callback='parse_item', follow=True),
#     )

#     def parse_item(self, response):
#         soup_str = self.get_text(response)
#         yield {
#             "url": response.url,
#             "soup": soup_str,
#         }

#     def get_text(self, response):
#         soup = BeautifulSoup(response.body, 'html.parser')
#         [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
#         visible_text = soup.getText()
#         visible_text = visible_text.replace("\n", " ")
#         visible_text = visible_text.replace("\t", " ")
#         return visible_text
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

class TestSpider(CrawlSpider):
    name = "testspider"
    allowed_domains = ["opendatawatch.com"]
    start_urls = ["https://opendatawatch.com/"]

    # Define denial terms using regex for case-insensitive matching and substrings
    deny_terms = [
        re.escape(term) for term in [
            r"(?i)contact",
            r"(?i)privacy",
            # Add other terms here as needed
        ]
    ]

    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=deny_terms, unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
        if 'text/html' not in content_type:
            self.logger.info(f"Skipping {response.url} due to content type: {content_type}")
            return

        soup_str = self.get_text(response)
        yield {
            "url": response.url,
            "soup": soup_str,
        }

    def get_text(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        visible_text = visible_text.replace("\n", " ")
        visible_text = visible_text.replace("\t", " ")
        return visible_text
