from pylinkedin import search
from pylinkedin.db import mongodb_provider as mgp

import json
import os
from dotenv import load_dotenv
load_dotenv()

KEY_WORD = os.getenv('KEY_WORD')
LIAT = os.getenv('LIAT')
MONGODB_URL = os.getenv('MONGODB_URL')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME')

# To crawler multiple profiles with searching by a key word
data = search.crawl(keyword=KEY_WORD, li_at_cookie=LIAT, debug=True)

# Save to mongodb
code = mgp.save(connection_string=MONGODB_URL, db=MONGODB_DB_NAME, collection=MONGODB_COLLECTION_NAME, data=data, debug=True)
print(code)