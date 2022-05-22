# wevliegen
First take-off with Weaviate.

# Prep

Export the connection uris for both Weaviate and MongoDB to system variables `weaviate_uri` and `atlas_uri`. Example for MongoDB Atlas, do simialr for Weaviate.

On MacOS, Linux `export atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/database`

On Windows `set atlas_uri=mongodb+srv://something:secret@some.place.mongodb.net/database`

## Weaviate

Create a Weaviate cluster.

See https://weaviate.io/developers/weaviate/current/client-libraries/python.html

`python3 -m pip install weaviate-client`

## MongoDB

A MongoDB database with some content either local or Atlas.

# Code

See `mongodb2weaviate.py`. Uses pymongo to retrieve documents from MongoDB and pass to Weaviate.
