from pylinkedin import profile
from pylinkedin.db import mongodb_provider as mgp

import json
import os
from dotenv import load_dotenv
load_dotenv()

PID = os.getenv('PID')
PTYPE = os.getenv('PTYPE')
LIAT = os.getenv('LIAT')
MONGODB_URL = os.getenv('MONGODB_URL')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME')

# To crawler one profile
data = profile.crawl(profile_id=PID, profile_type=PTYPE, li_at_cookie=LIAT, debug=True)

# Save to mongo db
code = mgp.save(connection_string=MONGODB_URL, db=MONGODB_DB_NAME, collection=MONGODB_COLLECTION_NAME, data=data, debug=True)
print(code)