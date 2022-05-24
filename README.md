# wevliegen
First take-off with Weaviate.

# Prep

Export the connection uris for both Weaviate and MongoDB to system variables `WEAVIATE_URI` and `ATLAS_URI`. Example for MongoDB Atlas, do simialr for Weaviate.

## On MacOS, Linux

`export ATLAS_URI=mongodb+srv://something:secret@some.place.mongodb.net/database` or `export ATLAS_URI=mongodb://localhost`

`export WEAVIATE_URI=http://localhost:8080`

On Windows `set ATLAS_URI=mongodb+srv://something:secret@some.place.mongodb.net/database`


## Weaviate

### WCS

Create a Weaviate cluster.

### Local

Configured a yml file usign wizard at https://weaviate.io/developers/weaviate/current/getting-started/installation.html

Download yml file

`curl -o docker-compose.yml "https://configuration.semi.technology/v2/docker-compose/docker-compose.yml?enterprise_usage_collector=false&gpu_support=false&media_type=text&modules=modules&ner_module=false&qna_module=false&runtime=docker-compose&spellcheck_module=false&text_module=text2vec-transformers&transformers_model=sentence-transformers-paraphrase-multilingual-mpnet-base-v2&weaviate_version=v1.13.2"`

Check if docker is started (using Docker Desktop on my Mac).

Run `docker-compose up -d`

Weaviate is now running at localhost:8080

http://localhost:8080/v1

### Client

See https://weaviate.io/developers/weaviate/current/client-libraries/python.html

`python3 -m pip install weaviate-client`

## MongoDB

A MongoDB database with some content either local or Atlas.

# Code

See `mongodb2weaviate.py`. Uses `pymongo` to retrieve documents from MongoDB and `weaviate` to insert into Weaviate.

Run `python3 mongodb2weaviate.py`
