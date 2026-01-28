# ps-client

Minimal client to read configuration from AWS Parameter Store.
A key motivation for this library is to standardise on the use of configuration across services.

### Usage

#### Pre-requisites

- The library presumes credentials are available using one of the [standard AWS credential mechanisms](https://boto3.amazonaws.com/v1/documentation/api/1.18.54/guide/credentials.html#:~:text=The%20mechanism%20in%20which%20Boto3,client()%20method).
- The following convention is followed for keys in parameter store: `/<environment>/<service>/<key>`
  - For example, `/test/service/foo` is the key for the `foo` configuration value for the `service` service, in the `test` environment.

```shell
$ uv add git+https://github.com/km-ox/ps-client --tag foo
$ uv add ps-client
```

```python
# example.py

from ps_client import ConfigClient

client = ConfigClient(environment='test', service='service', region='us-east-1')
foo = client.get('foo')
```

- A `KeyError` will be raised if the key is not found. The library does not introduce new error types.