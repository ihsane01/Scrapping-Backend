import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# le nom de bdd
db = client['datajournals']

# le nom de collection
collection = db['data']
# collection = db['scopus']

# le chemin de data sous form json
with open('data.json') as file:
    file_data = json.load(file)
collection.insert_many(file_data)
client.close()
