import json
import re
import os
from dotenv import load_dotenv
import weaviate
from bson.json_util import dumps
from pymongo import MongoClient

load_dotenv()

# Weaviate
weaviate_uri = os.getenv('WEAVIATE_URI')
weaviateClient = weaviate.Client(weaviate_uri)
batch_size = 1
weaviateClient.batch(batch_size=batch_size)
# get the full schema as example
#client_schema = weaviateClient.schema.get()
# delete all schemas use with care...
weaviateClient.schema.delete_all()
#print(client_schema)

# Atlas
atlas_uri = os.getenv('ATLAS_URI')
mongoClient = MongoClient(atlas_uri)
db_name='datafitness'
col_name='foldertrees'
col_name='contents'
db = mongoClient[db_name]

filter = {}
limit = 0 # 0 is no limit

documents = list(db[col_name].find(filter).limit(limit))
#documents = db[col_name].find(filter).limit(limit)
#documents = documents[:1]

with weaviateClient.batch as batch:
    for document in documents:
        document = dumps(document)
        document = document.replace(r'\n',' ').replace(r'\r\n',' ').replace(r'\r',' ')
        document = document.encode('ascii', 'ignore')
        document = document.decode()
        document = json.loads(document)
        document['content'] = ' '.join(document['content'].split())
        document['content'] = ' '.join(document['content'].splitlines())
        document['content'] = re.sub(r'[^\x00-\x7F]+',' ', document['content'])
        document['metadata'] = 'TODO'
        id = document['_id']['$oid']
        document['objectId'] = id
        document.pop('_id')
        #print(document)
        weaviateClient.batch.add_data_object(data_object=document,class_name=col_name)

    #response = weaviateClient.data_object.create(data_object = document,class_name = 'Content')
    #print(response)
