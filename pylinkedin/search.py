from . import profile
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
    path =  str(path) + "\\search_rules.json"

    with open(path, 'r') as f:
        rules = json.load(f)

    return rules

def crawl(keyword=None, profile_type='profil', li_at_cookie=None, headless=True, debug=False):
    if not keyword:
        if debug: print(f'keyword is required')
        return None

    data = []
    profiles = []

    if debug: print(f'[PYLINKEDIN] Load search_rules.json data')
    obj = load_rules()
    url = str(obj[profile_type]['url_placeholder']).format(keyword)
    url_profile_base = str(obj[profile_type]['url_profile_base'])
    
    # Open Chrome & get to target
    if debug: print(f'[PYLINKEDIN] Open new instance - Chrome')
    driver = chrome.get_instance(headless=headless)
    if debug: print(f'[PYLINKEDIN] Get to target page: {url}')
    driver.get(url)
    if debug: print(f'[PYLINKEDIN] Adding cookie')
    driver = add_cookie(driver, li_at_cookie)
    driver.get(url) # have to refresh to apply cookie

    # Browse the page
    if debug: print(f'[PYLINKEDIN] Browsing the page')
    chrome.browse(driver=driver, element_id='profile-nav-item')

    # Get list profile ids    
    if debug: print(f'[PYLINKEDIN] Get profile ids')
    pids = driver.find_elements_by_xpath(obj[profile_type]['xpath_profiles'])    
    # TBU: get to other page(s)...
    # ...
    for pid in pids:
        href = pid.get_attribute('href')
        if 'keywords' in href:
            continue
        profiles.append(href.replace(url_profile_base,'').replace('/',''))

    if debug: print(f'[PYLINKEDIN] Loop the list and crawl data')
    for pid in profiles:
        pdata = profile.crawl(driver=driver,profile_id=pid, profile_type=profile_type, li_at_cookie=li_at_cookie, headless=headless, debug=debug)
        data.append(pdata)

    return data