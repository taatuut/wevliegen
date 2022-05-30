import json
from pydoc import doc
import re
import os
from dotenv import load_dotenv
import weaviate
from bson.json_util import dumps
from pymongo import MongoClient
import sys

load_dotenv()

def prepMDB2WV8(document):
    # prepping the document from MongoDB for insertion into Weaviate.
    # TODO: check what is needed, bit messy currently but works...
    document = dumps(document)
    document = document.replace(r'\n',' ').replace(r'\r\n',' ').replace(r'\r',' ')
    document = document.encode('ascii', 'ignore')
    document = document.decode()
    document = json.loads(document)
    # TODO: gracefully fail if fields like content/metadata/$oid don't exist
    content = ' '.join(document['content'].split())
    content = ' '.join(content.splitlines())
    document['content'] = re.sub(r'[^\x00-\x7F]+',' ', content)
    # TODO: Weaviate does not support (nested) object as a property as in metadata
    # below code does create valid clean json, but for now replacing with a dummy string...
    metadata = dumps(document['metadata'])
    metadata = ' '.join(dumps(metadata).split())
    metadata = ' '.join(metadata.splitlines())
    metadata = re.sub(r'[^\x00-\x7F]+',' ', metadata)
    # NOTE: commenting next line enables inserting metadata as string
    metadata = json.loads(metadata)
    document['metadata'] = metadata
    document['metadata'] = 'DUMMY'
    id = document['_id']['$oid']
    document['objectId'] = id
    document.pop('_id')
    #print(document)
    return document

# Weaviate
weaviate_uri = os.getenv('WEAVIATE_URI')
weaviateClient = weaviate.Client(url=weaviate_uri,timeout_config=(5,255))
batch_size = 1
weaviateClient.batch.configure(batch_size=batch_size)
# To get the full schema
#client_schema = weaviateClient.schema.get()
# deletes all schemas use with care...
weaviateClient.schema.delete_all()
# not defining a schema upfront so Weaviate will auto generate one
 
# Atlas
atlas_uri = os.getenv('ATLAS_URI')
mongoClient = MongoClient(atlas_uri)
db_name=os.getenv('ATLAS_DATABASE')
col_name=os.getenv('ATLAS_COLLECTION')
class_name=col_name.replace('.','_')
db = mongoClient[db_name]
filter = {}
limit = 15 # 0 is no limit
i = 0 # lousy counter keeping track of documents inserted into Weaviate
documents = list(db[col_name].find(filter).limit(limit))
print(len(documents))
#sys.exit()

# Batch load documents from MongoDB into Weaviate
with weaviateClient.batch as batch:
    for document in documents:
        document = prepMDB2WV8(document)
        response = weaviateClient.batch.add_data_object(data_object=document,class_name=class_name)
        i = i + 1
        print(i)

print(i,"documents inserted into Weaviate class",class_name,"from MongoDB collection",col_name)