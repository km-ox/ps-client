# ps-client

Minimal client to read configuration from AWS Parameter Store.

### Usage

#### Pre-requisites

Use of the client library presumes credentials are available using one of the [standard AWS credential mechanisms](https://boto3.amazonaws.com/v1/documentation/api/1.18.54/guide/credentials.html#:~:text=The%20mechanism%20in%20which%20Boto3,client()%20method).

```shell
$ pip install ps-client
```

```python
# example.py

from ps_client import ConfigClient

client = ConfigClient()
foo = client.get('foo')
```