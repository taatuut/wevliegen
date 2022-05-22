# wevliegen
First take-off with Weaviate.

# Prep

Export the connection uris for both Weaviate and MongoDB to system variables `WEAVIATE_URI` and `ATLAS_URI`. Example for MongoDB Atlas, do simialr for Weaviate.

On MacOS, Linux `export ATLAS_URI=mongodb+srv://something:secret@some.place.mongodb.net/database`

On Windows `set ATLAS_URI=mongodb+srv://something:secret@some.place.mongodb.net/database`

## Weaviate

Create a Weaviate cluster.

See https://weaviate.io/developers/weaviate/current/client-libraries/python.html

`python3 -m pip install weaviate-client`

## MongoDB

A MongoDB database with some content either local or Atlas.

# Code

See `mongodb2weaviate.py`. Uses pymongo to retrieve documents from MongoDB and pass to Weaviate.
