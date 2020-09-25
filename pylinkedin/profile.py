from .browser import chrome
from bs4 import BeautifulSoup

import re
import json


def add_cookie(driver, li_at_cookie):
    driver.add_cookie({
        'name': 'li_at',
        'value': li_at_cookie,
        'domain': '.www.linkedin.com'
    })
    return driver

def extract_soup(soup, fields_to_extract):
    out = dict()

    code_snippets = soup.findAll("code")

    for output_dict_key, extract in fields_to_extract.items():
        output_dict_key = output_dict_key.rsplit('.', 1)[1]
        out[output_dict_key] = list()

    for code in code_snippets:
        if 'com.linkedin.voyager' in code.text.strip():
            data = json.loads(code.text.strip())

            if 'included' in data:
                data = data['included']

                for rule_key, rule in fields_to_extract.items():
                    for sub_dataset in data:
                        if '$type' in sub_dataset:

                            if sub_dataset['$type'] == rule_key:
                                temp = dict()

                                for field in rule['fields']:
                                    if field in sub_dataset:
                                        temp[field] = sub_dataset[field]

                                if 'custom_fields' in rule:
                                    for k, field in rule['custom_fields'].items():
                                        try:
                                            temp[k] = re.search(field['regex'], temp[field['field']],
                                                                re.IGNORECASE).group(1)
                                        except:
                                            pass

                                if rule['list']:
                                    out[rule_key.rsplit('.', 1)[1]].append(temp)
                                else:
                                    out[rule_key.rsplit('.', 1)[1]] = temp

                        if '$recipeTypes' in sub_dataset:

                            for rtype in sub_dataset['$recipeTypes']:

                                if rtype == rule_key:
                                    temp = dict()
                                    for field in rule['fields']:
                                        if field in sub_dataset:
                                            temp[field] = sub_dataset[field]

                                    if 'custom_fields' in rule:
                                        for k, field in rule['custom_fields'].items():
                                            try:
                                                temp[k] = re.search(field['regex'], temp[field['field']],
                                                                    re.IGNORECASE).group(1)
                                            except:
                                                pass

                                    if rule['list']:
                                        out[rule_key.rsplit('.', 1)[1]].append(temp)
                                    else:
                                        out[rule_key.rsplit('.', 1)[1]] = temp

    return out

def crawl(profile_id=None, li_at_cookie=None, headless=True, debug=False):
    if profile_id is None:
        if debug: print(f'Profile ID is required')
        return None

    if li_at_cookie is None:
        if debug: print(f'Cookie (li_at_cookie) is required')
        return None

    obj = {}
    url = f'https://www.linkedin.com/in/{profile_id}/'
    # url = 'https://www.linkedin.com/search/results/people/?keywords=database&origin=GLOBAL_SEARCH_HEADER'
    
    # Open Chrome & get to target
    if debug: print(f'[PYLINKEDIN] Open new instance - Chrome')
    driver = chrome.get_instance(headless=headless)
    if debug: print(f'[PYLINKEDIN] Get to target page')
    driver.get(url)
    if debug: print(f'[PYLINKEDIN] Adding cookie')
    driver = add_cookie(driver, li_at_cookie)
    driver.get(url) # have to refresh to apply cookie

    # Browse the page
    if debug: print(f'[PYLINKEDIN] Browsing the page')
    chrome.browse(driver=driver, element_id='profile-nav-item')

    # Browse the page
    if debug: print(f'[PYLINKEDIN] Get page source')
    page_source = chrome.get_page_source(driver=driver)
    soup = BeautifulSoup(page_source, 'html.parser')

    result = extract_soup(soup=soup, fields_to_extract=None)
    print(result)

    # to be continued....

    # Result
    return obj