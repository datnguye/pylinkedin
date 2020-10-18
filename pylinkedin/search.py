from . import profile
import re
import json
from pathlib import Path
import os

def load_rules():
    rules = {}
    
    path = Path(os.path.dirname(os.path.abspath(__file__)))
    path =  str(path) + "\\search_rules.json"

    with open(path, 'r') as f:
        rules = json.load(f)

    return rules

def crawl(keyword=None, profile_type='profil', debug=False):
    if not keyword:
        if debug: print(f'keyword is required')
        return None

    data = []

    if debug: print(f'[PYLINKEDIN] Load search_rules.json data')
    obj = load_rules()
    url = str(obj[profile_type]['url_placeholder']).format(profile_id)
    
    if debug: print(f'[PYLINKEDIN] Get profile list')

    if debug: print(f'[PYLINKEDIN] Loop the list and crawl data')
    

    return data