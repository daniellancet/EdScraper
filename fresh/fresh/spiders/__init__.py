# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# import scrapy
# import tldextract
# import pandas as pd
# import json


# def get_root_domain(url):
#     extracted = tldextract.extract(url)
#     root_domain = f"{extracted.domain}.{extracted.suffix}"
#     return root_domain

# class LinkSpider(scrapy.Spider):
#     name = "simplespider"

#     def __init__(self, csv_input=None, *args, **kwargs):
#         """
#         Overrides default constructor to set start_urls.
#         """
#         super(LinkSpider, self).__init__(*args, **kwargs)
#         if csv_input:
#             self.df = pd.read_csv(csv_input)
#             self.start_urls = self.df["url"].tolist()
#         else:
#             self.start_urls = []

#     def start_requests(self):
#         # Override start_requests to customize initial requests
#         for url in self.start_urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         # Print the status code of the response
#         status = response.status
#         true_url = response.url
#         input_url = response.meta["download_slot"]
#         match = get_root_domain(input_url) == get_root_domain(true_url)
        
#         yield {
#             "status": status,
#             "true_url": true_url,
#             "input_url": input_url,
#             "match": match
#         }
    
#     def closed(self, reason):
#         # Called when the spider closes
#         # Output the results as JSON
#         output_filename = 'output.json'
#         with open(output_filename, 'w') as f:
#             f.write('[\n')
#             for item in self.parse(response=None):
#                 f.write(f'  {json.dumps(item)},\n')
#             f.write(']\n')
#         self.log(f'Saved JSON output to {output_filename}')






import scrapy
import json
import pandas as pd
import tldextract

def get_root_domain(url):
    extracted = tldextract.extract(url)
    root_domain = f"{extracted.domain}.{extracted.suffix}"
    return root_domain

class LinkSpider(scrapy.Spider):
    name = "simplespider"

    def __init__(self, csv_input=None, *args, **kwargs):
        """
        Overrides default constructor to set start_urls.
        """
        super(LinkSpider, self).__init__(*args, **kwargs)
        if csv_input:
            self.df = pd.read_csv(csv_input)
            self.start_urls = self.df["url"].tolist()
        else:
            self.start_urls = []

        self.items = []  # Initialize an empty list for storing items

    def start_requests(self):
        # Override start_requests to customize initial requests
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'input_url': url})

    def parse(self, response):
        # Process the response and yield items
        status = response.status
        true_url = response.url
        input_url = response.meta["input_url"]
        match = get_root_domain(input_url) == get_root_domain(true_url)
        
        item = {
            "status": status,
            "true_url": true_url,
            "input_url": input_url,
            "match": match
        }
        self.items.append(item)  # Add the item to the list

    def closed(self, reason):
        # Called when the spider closes
        # Output the items as JSON
        output_filename = 'output.json'
        with open(output_filename, 'w') as f:
            json.dump(self.items, f, indent=2)
        self.log(f'Saved JSON output to {output_filename}')
