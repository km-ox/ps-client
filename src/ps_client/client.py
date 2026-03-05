import boto3


class ConfigClient:
    def __init__(self, region: str, environment: str, service: str | None = None):
        self.environment = environment
        self.service = service
        self.client = boto3.client("ssm", region_name=region)

    def get(self, key: str, service: str | None = None) -> str:
        return self._get_parameter(key, service)

    def get_secret(self, key: str, service: str | None = None) -> str:
        return self._get_parameter(key, service, decrypt=True)

    def _get_parameter(
        self,
        key: str,
        service: str | None = None,
        decrypt: bool = False,
    ) -> str:
        _service = service or self.service
        _key = get_key(key, self.environment, _service)
        try:
            response = self.client.get_parameter(Name=_key, WithDecryption=decrypt)
            parameter_type = response["Parameter"]["Type"]
            if not decrypt and parameter_type == "SecureString":
                raise ValueError(f"warning: [{key}] is encrypted.")

            return response["Parameter"]["Value"]
        except self.client.exceptions.ParameterNotFound as e:
            raise KeyError(e) from e


def get_key(key: str, environment: str, service: str):
    if service is None:
        raise ValueError("service is required.")
    return f"/{environment}/{service}/{key}"
