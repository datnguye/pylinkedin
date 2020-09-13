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
    
    # Open Chrome & get to target
    if debug: print(f'[PYLINKEDIN] Open new instance - Chrome')
    driver = chrome.get_instance(headless=headless)
    if debug: print(f'[PYLINKEDIN] Get to target page')
    driver.get(f'https://www.linkedin.com/in/{profile_id}/')
    if debug: print(f'[PYLINKEDIN] Adding cookie')
    driver = add_cookie(driver, li_at_cookie)

    # 

    # Result
    return obj