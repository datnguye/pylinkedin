# pylinkedin
This is to crawl LinkedIn profile

Virtual enviroment:
```
python -m venv env
```

Activate virtual env:
```
.\env\Scripts\activate
OR source env/bin/activate (linux)
```

Install dependencies:
```
pip install -r requirements.txt
```

Create dotenv file as below template:
```
PID=tuiladat
PTYPE=profil
LIAT=your_li_at_cookie

MONGODB_URL=your_mongodb_url
MONGODB_DB_NAME=linkedin
MONGODB_COLLECTION_NAME=raw_data
```