# pylinkedin
This is to crawl LinkedIn profile

#### Virtual enviroment:
```
python -m venv env
```

#### Activate virtual env:
```
.\env\Scripts\activate
OR source env/bin/activate (linux)
```

#### Install dependencies:
```
pip install -r requirements.txt
```

#### Create dotenv file as below template:
##### To use for crawling one target IDs:
```
PID=tuiladat
PTYPE=profil
LIAT=your_li_at_cookie

MONGODB_URL=your_mongodb_url e.g. mongodb://linkedin:linkedin@localhost:27017/?authSource=linkedin
MONGODB_DB_NAME=linkedin
MONGODB_COLLECTION_NAME=raw_data
```

##### To use for crawling by a searching keyword
```
KEY_WORD=database developer
LIAT=your_li_at_cookie

MONGODB_URL=your_mongodb_url e.g. mongodb://linkedin:linkedin@localhost:27017/?authSource=linkedin
MONGODB_DB_NAME=linkedin
MONGODB_COLLECTION_NAME=raw_data
```


###### In aboves,
** KEY_WORD: This is the keyword to be based on to have list of target IDs, then to crawl multiple ones
** PID: This is LinkedIn ID of target profile
** PTYPE: Profile type whether it's Person (profil) or Company (company)
** LIAT: This is the cookie used to bypass authentication
** MONGODB_URL: Mongo DB URI, please see references via https://docs.mongodb.com/manual/reference/connection-string/
** MONGODB_DB_NAME: Mongo DB name
** MONGODB_COLLECTION_NAME: Collection name