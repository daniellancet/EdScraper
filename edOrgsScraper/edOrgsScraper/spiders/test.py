import pandas as pd
from urllib.parse import urlparse

df = pd.DataFrame({"ein": [38, 31], "url": ["https://empowerillinois.org/", "http://www.academicintegrity.org/"]})

def ein_url_map(df):
    url_lst = df["url"].to_list()
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




print(ein_url_map(df))
