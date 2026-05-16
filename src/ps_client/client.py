import boto3


class ConfigClient:
    def __init__(self, region: str, environment: str, service: str | None = None):
        self.environment = environment
        self.service = service
        self.ssm_client = boto3.client("ssm", region_name=region)
        self.secretsmanager_client = boto3.client("secretsmanager", region_name=region)

    def get(self, key: str, service: str | None = None) -> str:
        return self._get_parameter(key, service)

    def get_sm_secret(self, key: str) -> str | None:
        try:
            secret_arn = self.secretsmanager_client.describe_secret(SecretId=f"/{self.environment}/{key}")["ARN"]
            if secret_arn is not None:
                return self.secretsmanager_client.get_secret_value(SecretId=secret_arn)["SecretString"]
        except self.secretsmanager_client.exceptions.ResourceNotFoundException:
            raise KeyError(f"/{self.environment}/{key} not found.") from None

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
            response = self.ssm_client.get_parameter(Name=_key, WithDecryption=decrypt)
            parameter_type = response["Parameter"]["Type"]
            if not decrypt and parameter_type == "SecureString":
                raise ValueError(f"warning: [{key}] is encrypted.")

            return response["Parameter"]["Value"]
        except self.ssm_client.exceptions.ParameterNotFound as e:
            raise KeyError(e) from e


def get_key(key: str, environment: str, service: str):
    if service is None:
        raise ValueError("service is required.")
    return f"/{environment}/{service}/{key}"
