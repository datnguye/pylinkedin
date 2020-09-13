from .browser import chrome

def crawl(profile_id=None, headless=True, debug=False):
    if profile_id is None:
        return None

    obj = {}
    
    # Open Chrome & get to target
    if debug: print(f'[PYLINKEDIN] Open new instance - Chrome')
    driver = chrome.get_instance(headless=headless)

    # Result
    return obj