# ps-client

Minimal client to read configuration from AWS Parameter Store.
Key motivation is to standardise on how configuration is consumed by services, following a simple scheme to organise keys (by environment and consuming service or app).

### Usage

#### Pre-requisites

- We presume credentials are made available using one of the [standard AWS credential mechanisms](https://boto3.amazonaws.com/v1/documentation/api/1.18.54/guide/credentials.html#:~:text=The%20mechanism%20in%20which%20Boto3,client()%20method).
- We follow this convention for keys in parameter store: `/<environment>/<service>/<key>`
  - For example, `/test/service/foo` is the key for the `foo` configuration value for `service`, in the `test` environment.

```shell
$ uv add git+https://github.com/km-ox/ps-client
```

```python
# example.py
from ps_client import ConfigClient
client = ConfigClient(environment='test', service='service', region='us-east-1')

# get a cleartext value
foo = client.get('foo')

# get a secret value
secret = client.get_secret('bar')
```

- The library does not introduce new error types.
- A `KeyError` is raised for missing keys. 
- (In a departure from the underlying AWS `get-parameter` API) the library raises a `ValueError` when `get` is used to read an encrypted value.

### Known limitations

- The underlying AWS API throttles requests when reading many values in a short period of time.