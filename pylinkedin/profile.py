from .browser import chrome

def add_cookie(driver, li_at_cookie):
    driver.add_cookie({
        'name': 'li_at',
        'value': li_at_cookie,
        'domain': '.www.linkedin.com'
    })
    return driver

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
    print(page_source)

    # to be continued....

    # Result
    return obj