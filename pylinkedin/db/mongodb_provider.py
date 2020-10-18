from pymongo import MongoClient
from datetime import datetime

USE_EXISTING_CONNECTION = 'USE_EXISTING'

def get_filter_object(document={}, keys=[]):
    filters = {}
    for k in keys:
        filters[k] = document[k]
    return filters

def save(connection_string=USE_EXISTING_CONNECTION, db='default', collection='default', data=[], debug=False):
    if connection_string is None or not data:
        return (-1,'Not configurable')

    try:
        if connection_string != USE_EXISTING_CONNECTION:
            client = MongoClient(connection_string)
            db = client[db]
            
        coll = db[collection]
    except Exception as e:
        if debug: print(f'Could not connect to server with message: {e}')
        return (-1, str(e))

    # # purge all existing raw data
    # r = coll.delete_many({})
    # if debug: print(f'Purged all documents from {collection} with info = {str(r)}')
    
    # save raw data
    r = coll.insert_many(data)
    if debug: print(f'Inserted into {collection} with row count = {len(r.inserted_ids)}')
    r = coll.update_many({'created_at': {'$exists': False}}, {'$set' : { "created_at" : datetime.now()}}, upsert=False)
    if debug: print(f'Timestamp updated {collection} with row count = {r.matched_count}')
    
    return (0,'OK')