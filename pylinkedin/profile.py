from .browser import chrome
from bs4 import BeautifulSoup

import re
import json
from pathlib import Path
import os


def add_cookie(driver, li_at_cookie):
    driver.add_cookie({
        'name': 'li_at',
        'value': li_at_cookie,
        'domain': '.www.linkedin.com'
    })
    return driver

def load_rules():
    rules = {}
    
    path = Path(os.path.dirname(os.path.abspath(__file__)))
    path =  str(path) + "\\profile_rules.json"

    with open(path, 'r') as f:
        rules = json.load(f)

    return rules

def extract_soup(soup, fields_to_extract):
    out = dict()

    code_snippets = soup.findAll('code')

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
                                                temp[k] = re.search(field['regex'], temp[field['field']], re.IGNORECASE).group(1)
                                            except:
                                                pass

                                    if rule['list']:
                                        out[rule_key.rsplit('.', 1)[1]].append(temp)
                                    else:
                                        out[rule_key.rsplit('.', 1)[1]] = temp

    return out

def crawl(driver=None, profile_id=None, profile_type='profil', li_at_cookie=None, headless=True, debug=False):
    """ profile_type = 'profil' or 'company'"""
    if profile_id is None:
        if debug: print(f'Profile ID is required')
        return None

    if li_at_cookie is None:
        if debug: print(f'Cookie (li_at_cookie) is required')
        return None

    if debug: print(f'[PYLINKEDIN] Load profile_rules.json data')
    obj = load_rules()
    url = str(obj[profile_type]['url_placeholder']).format(profile_id)
    
    # Open Chrome & get to target
    if debug: print(f'[PYLINKEDIN] Open new instance - Chrome')
    if driver is None:
        driver = chrome.get_instance(headless=headless)
    if debug: print(f'[PYLINKEDIN] Get to target page: {url}')
    driver.get(url)
    if debug: print(f'[PYLINKEDIN] Adding cookie')
    driver = add_cookie(driver, li_at_cookie)
    driver.get(url) # have to refresh to apply cookie

    # Browse the page
    if debug: print(f'[PYLINKEDIN] Browsing the page')
    chrome.browse(driver=driver, element_id='profile-nav-item')

    # Get page source
    if debug: print(f'[PYLINKEDIN] Get page source')
    page_source = chrome.get_page_source(driver=driver)
    
    # Parsing
    if debug: print(f'[PYLINKEDIN] Parse info')
    soup = BeautifulSoup(page_source, 'html.parser')
    rules = obj[profile_type]['extract_rules']
    result = extract_soup(soup=soup, fields_to_extract=rules)

    result['profile_id'] = profile_id
    result['profile_type'] = profile_type

    result = json.dumps(result).replace('$', '')
    return [json.loads(result)]