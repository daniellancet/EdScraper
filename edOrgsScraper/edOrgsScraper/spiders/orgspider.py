# import scrapy
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from Levenshtein import ratio
# import pandas as pd

# def match_allowed_domains(allowed_domains, url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc.lower()

#     matched_domains = [allowed_domain for allowed_domain in allowed_domains if domain.endswith(allowed_domain.lower())]
    
#     return matched_domains

# def match_allowed_domains_lev(allowed_domains, url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc.lower()

#     best_match = None
#     best_score = 0

#     for allowed_domain in allowed_domains:
#         score = ratio(domain, allowed_domain.lower())
#         print(score)
#         if score > best_score:
#             best_score = score
#             best_match = allowed_domain

#     return best_match


# def ein_url_map(df):
#     url_lst = df["urls"].to_list()
#     ein_lst = df["ein"].to_list()
#     domain_dict = {}
#     for i in range(len(url_lst)): 
#         url = url_lst[i]
#         ein = ein_lst[i]
#         parsed_url = urlparse(url)
#         domain = parsed_url.netloc.lower()
#         domain_dict[domain] = ein
#     return domain_dict

# def get_allowed_domains(domain_dict):
#     return domain_dict.keys()

# def get_matched_allowed_domain(allowed_domains, url, allowed_domain_id_map):
#     match_lst = match_allowed_domains(allowed_domains, url)
#     best_match = match_allowed_domains_lev(match_lst, url)
#     return allowed_domain_id_map[best_match]



# class OrgSpider(scrapy.Spider):
#     name = "orgspiders"
#     df = pd.read_csv("/Users/daniellancet/Desktop/scrapy_install/EdScraper/edOrgsScraper/edOrgsScraper/test.csv")
#     ein_domain_dict = ein_url_map(df)
#     print(ein_domain_dict)
#     allowed_domains = get_allowed_domains(ein_domain_dict)
#     start_urls = df["urls"].to_list()
#     #custom_settings = {"RETRY_TIMES": 2, "DEPTH_LIMIT": 2}
    
#     def parse(self, response):
#         soup_str = self.get_text(response)
#         yield {
#             "start_link": get_matched_allowed_domain(self.allowed_domains, response.url, self.ein_domain_dict),
#             "url": response.url, 
#             "soup": soup_str,
#         }

#         for href in response.xpath("//a/@href").getall():
#             next_page = response.urljoin(href)
#             if self.is_allowed_domain(next_page):
#                 yield scrapy.Request(next_page, self.parse)

#     def is_allowed_domain(self, url):
#         """ Check if the url belongs to the allowed domain """
#         return any(domain in url for domain in self.allowed_domains)
    
#     def get_text(self, response):
#             soup = BeautifulSoup(response.body)
#             [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
#             visible_text = soup.getText()
#             visible_text = visible_text.replace("\n", " ")
#             visible_text = visible_text.replace("\t", " ")
#             return visible_text

# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
# from Levenshtein import ratio
# import pandas as pd

# def match_allowed_domains(allowed_domains, url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc.lower()
#     matched_domains = [allowed_domain for allowed_domain in allowed_domains if domain.endswith(allowed_domain.lower())]
#     return matched_domains

# def match_allowed_domains_lev(allowed_domains, url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc.lower()
#     best_match = None
#     best_score = 0
#     for allowed_domain in allowed_domains:
#         score = ratio(domain, allowed_domain.lower())
#         if score > best_score:
#             best_score = score
#             best_match = allowed_domain
#     return best_match

# def ein_url_map(df):
#     url_lst = df["urls"].to_list()
#     ein_lst = df["ein"].to_list()
#     domain_dict = {}
#     for i in range(len(url_lst)):
#         url = url_lst[i]
#         ein = ein_lst[i]
#         parsed_url = urlparse(url)
#         domain = parsed_url.netloc.lower()
#         domain_dict[domain] = ein
#     return domain_dict

# def get_allowed_domains(domain_dict):
#     return domain_dict.keys()

# def get_matched_allowed_domain(allowed_domains, url, allowed_domain_id_map):
#     match_lst = match_allowed_domains(allowed_domains, url)
#     best_match = match_allowed_domains_lev(match_lst, url)
#     return allowed_domain_id_map[best_match]

# class OrgSpider(CrawlSpider):
#     name = "orgspiders"
#     df = pd.read_csv("/Users/daniellancet/Desktop/scrapy_install/EdScraper/edOrgsScraper/edOrgsScraper/test.csv")
#     ein_domain_dict = ein_url_map(df)
#     allowed_domains = list(get_allowed_domains(ein_domain_dict))
#     start_urls = df["urls"].to_list()

#     rules = (
#         Rule(LinkExtractor(allow_domains=allowed_domains, unique=True), callback='parse_item', follow=True),
#     )

#     def parse_item(self, response):
#         soup_str = self.get_text(response)
#         yield {
#             "start_link": get_matched_allowed_domain(self.allowed_domains, response.url, self.ein_domain_dict),
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
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from Levenshtein import ratio
import pandas as pd
import re

def match_allowed_domains(allowed_domains, url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    matched_domains = [allowed_domain for allowed_domain in allowed_domains if domain.endswith(allowed_domain.lower())]
    return matched_domains

def match_allowed_domains_lev(allowed_domains, url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    best_match = None
    best_score = 0
    for allowed_domain in allowed_domains:
        score = ratio(domain, allowed_domain.lower())
        if score > best_score:
            best_score = score
            best_match = allowed_domain
    return best_match

def ein_url_map(df):
    url_lst = df["urls"].to_list()
    ein_lst = df["ein"].to_list()
    domain_dict = {}
    for i in range(len(url_lst)):
        url = url_lst[i]
        ein = ein_lst[i]
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        domain_dict[domain] = ein
    return domain_dict

def get_allowed_domains(domain_dict):
    return domain_dict.keys()

def get_matched_allowed_domain(allowed_domains, url, allowed_domain_id_map):
    match_lst = match_allowed_domains(allowed_domains, url)
    best_match = match_allowed_domains_lev(match_lst, url)
    return allowed_domain_id_map[best_match]

class OrgSpider(CrawlSpider):
    name = "orgspiders"
    df = pd.read_csv("/Users/daniellancet/Desktop/scrapy_install/EdScraper/edOrgsScraper/edOrgsScraper/test.csv").head(2.)
    ein_domain_dict = ein_url_map(df)
    allowed_domains = list(get_allowed_domains(ein_domain_dict))
    start_urls = df["urls"].to_list()

    import re

# Define denial terms using regex for case-insensitive matching and substrings
    deny_terms = [
        re.escape(term) for term in [
            r"(?i)contact",
            r"(?i)privacy",
            r"(?i)terms",
            r"(?i)disclaimer",
            r"(?i)careers",
            r"(?i)jobs",
            r"(?i)press",
            r"(?i)news",
            r"(?i)events",
            r"(?i)blog",
            r"(?i)donate",
            r"(?i)volunteer",
            r"(?i)faq",
            r"(?i)testimonials",
            r"(?i)sitemap",
            r"(?i)subscribe",
            r"(?i)advertise",
            r"(?i)sponsors",
            r"(?i)partners",
            r"(?i)resources",
            r"(?i)media",
            r"(?i)gallery",
            r"(?i)shop",
            r"(?i)store",
            r"(?i)membership",
            r"(?i)login",
            r"(?i)register",
            r"(?i)signup",
            r"(?i)support",
            r"(?i)advertisements",
            r"(?i)announcements",
            r"(?i)legal",
            r"(?i)accessibility",
            r"(?i)feedback",
            r"(?i)promotions",
            r"(?i)coupons",
            r"(?i)pricing",
            r"(?i)products",
            r"(?i)services",
            r"(?i)newsletter",
            r"(?i)social",
            r"(?i)awards",
            r"(?i)competitions",
            r"(?i)investor",
            r"(?i)webinars",
            r"(?i)surveys",
            r"(?i)forums",
            r"(?i)bylaws",
        ]
    ]


  
    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains, deny=deny_terms, unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup_str = self.get_text(response)
        yield {
            "start_link": get_matched_allowed_domain(self.allowed_domains, response.url, self.ein_domain_dict),
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
