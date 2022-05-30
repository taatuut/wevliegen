# wevliegen
First take-off with Weaviate.

# Prep

Export the connection uris for both Weaviate and MongoDB to system variables `WEAVIATE_URI` and `ATLAS_URI`. Example for MongoDB Atlas, do similar for Weaviate.

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

Some log info like printing the Weaviate uri and ids or number of inserted documents when successful could be returned (Weaviate batch mode does not retun id directly when adding to batch)

```
http://localhost:8080
ca4376d1-9625-403a-be27-35b1b1d3e288
87b05bde-0646-464e-aba3-bc8ebf29c3ab
53020390-2e69-4f83-bb32-12a7b7dd31d3
...
```

Just running for a complete MongoDB collection without setting the `batch_size` fails:

```
python3 mongodb2weaviate.py
Traceback (most recent call last):
  File "/Users/emilzegers/GitHub/taatuut/wevliegen/mongodb2weaviate.py", line 56, in <module>
    i = i + 1
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 898, in __exit__
    self.flush()
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 652, in flush
    result_objects = self.create_objects()
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 528, in create_objects
    response = self._create_data(
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 436, in _create_data
    raise ReadTimeout(message) from None
requests.exceptions.ReadTimeout: The 'objects' creation was cancelled because it took longer than the configured timeout of 55s. Try reducing the batch size (currently 198) to a lower value. Aim to on average complete batch request within less than 10s
```

So set `weaviateClient.batch(batch_size=<x>)`

Breaks with `batch_size=1` and longer timeout setting `timeout_config=(5,255)`

```
python3 mongodb2weaviate.py
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 699, in urlopen
    httplib_response = self._make_request(
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 445, in _make_request
    six.raise_from(e, None)
  File "<string>", line 3, in raise_from
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 440, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 1377, in getresponse
    response.begin()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 320, in begin
    version, status, reason = self._read_status()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 289, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 755, in urlopen
    retries = retries.increment(
  File "/usr/local/lib/python3.9/site-packages/urllib3/util/retry.py", line 532, in increment
    raise six.reraise(type(error), error, _stacktrace)
  File "/usr/local/lib/python3.9/site-packages/urllib3/packages/six.py", line 769, in reraise
    raise value.with_traceback(tb)
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 699, in urlopen
    httplib_response = self._make_request(
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 445, in _make_request
    six.raise_from(e, None)
  File "<string>", line 3, in raise_from
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 440, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 1377, in getresponse
    response.begin()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 320, in begin
    version, status, reason = self._read_status()
  File "/usr/local/Cellar/python@3.9/3.9.9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/http/client.py", line 289, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 415, in _create_data
    response = self._connection.post(
  File "/usr/local/lib/python3.9/site-packages/weaviate/connect/connection.py", line 314, in post
    return self._session.post(
  File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 590, in post
    return self.request('POST', url, data=data, json=json, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 542, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 655, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/adapters.py", line 498, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/emilzegers/GitHub/taatuut/wevliegen/mongodb2weaviate.py", line 58, in <module>
    i = i + 1
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 898, in __exit__
    self.flush()
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 652, in flush
    result_objects = self.create_objects()
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 528, in create_objects
    response = self._create_data(
  File "/usr/local/lib/python3.9/site-packages/weaviate/batch/crud_batch.py", line 428, in _create_data
    raise RequestsConnectionError('Batch was not added to weaviate.') from conn_err
requests.exceptions.ConnectionError: Batch was not added to weaviate.
```