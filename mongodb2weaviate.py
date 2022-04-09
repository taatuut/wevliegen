import json
import re
import weaviate
from bson.json_util import dumps
from pymongo import MongoClient

# Weaviate
weaviate_url = 'https://datafitness.semi.network'
weaviateClient = weaviate.Client(weaviate_url)
# get the full schema as example
client_schema = weaviateClient.schema.get()
# delete all schemas use with care...
#weaviateClient.schema.delete_all()
#print(client_schema)

# Atlas
atlas_uri = 'mongodb://localhost:27817'
mongoClient = MongoClient(atlas_uri)
db_name='datafitness'
col_name='foldertrees'
col_name='contents'
db = mongoClient[db_name]

filter = {}
limit = 2

documents = list(db[col_name].find(filter).limit(limit))
#documents = db[col_name].find(filter).limit(limit)
#documents = documents[:1]

for document in documents:
    document = dumps(document)
    document = document.replace(r"\n",'').replace(r"\r\n",'').replace(r"\r",'')
    document = document.encode("ascii", "ignore")
    document = document.decode()
    document = json.loads(document)
    document["content"] = " ".join(document["content"].split())
    document["content"] = " ".join(document["content"].splitlines())
    document["content"] = re.sub(r'[^\x00-\x7F]+','', document["content"])
    document["metadata"] = "TODO"
    id = document["_id"]["$oid"]
    document["objectId"] = id
    document.pop("_id")
    #print(document)

    response = weaviateClient.data_object.create(data_object = document,class_name = 'Content')
    print(response)
