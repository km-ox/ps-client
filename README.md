# ps-client

Minimal client to read configuration and secrets from AWS Parameter Store.
Now also reads secrets from AWS Secrets Manager.
Key motivation is to standardise on how configuration is consumed by services, following a simple scheme to organise keys (by environment and consuming service or app).

### Usage

#### Pre-requisites

- Specify at least the region and environment when constructing the client.
- We presume credentials are made available using one of the [standard AWS credential mechanisms](https://boto3.amazonaws.com/v1/documentation/api/1.18.54/guide/credentials.html#:~:text=The%20mechanism%20in%20which%20Boto3,client()%20method).
- We follow this convention for keys in parameter store: `/<environment>/<service>/<key>`
  - For example, `/test/service/foo` is the key for the `foo` configuration value for `service`, in the `test` environment.
- We follow this convention for secrets in parameter store: `/<environment>/<key>`

```shell
$ uv add git+https://github.com/km-ox/ps-client
```

- example for AWS Parameter Store

```python
from ps_client import ConfigClient
client = ConfigClient(environment='test', service='service', region='us-east-1')

# get a cleartext value
# key in Parameter Store is /test/service/foo
foo = client.get('foo')

# get a secret value
# key in Parameter Store is /test/service/bar
secret = client.get_secret('bar')
```

- example for AWS Secrets Manager 

```python
from ps_client import ConfigClient
client = ConfigClient(environment='test', region='us-east-1')

# get a secret value
# key in Secrets Manager is /test/foo
secret = client.get_sm_secret('foo')
```

- The library does not introduce new error types.
- A `KeyError` is raised for missing keys. 
- for Parameter Store: (In a departure from the underlying AWS `get-parameter` API) the library raises a `ValueError` when `get` is used to read an encrypted value.

### Known limitations

- The AWS API for Parameter Store throttles requests when reading many values in a short period of time.