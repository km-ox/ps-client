import boto3


class ConfigClient:

    def __init__(self, environment: str, service: str, region: str):
        self.environment = environment
        self.service = service
        self.client = boto3.client('ssm', region_name=region)

    def get(self, key: str) -> str:
        return self._get_parameter(key)

    def get_secret(self, key: str) -> str:
        return self._get_parameter(key, decrypt=True)

    def _get_parameter(self, key: str, decrypt: bool = False) -> str:
        try:
            response = self.client.get_parameter(
                Name=f"/{self.environment}/{self.service}/{key}",
                WithDecryption=decrypt
            )
            parameter_type = response['Parameter']['Type']
            if not decrypt and parameter_type == 'SecureString':
                raise ValueError(f"warning: [{key}] is encrypted.")

            return response['Parameter']['Value']
        except self.client.exceptions.ParameterNotFound as e:
            raise KeyError(e) from e
