import boto3


class ConfigClient:

    def __init__(self, environment: str, service: str, region: str):
        self.environment = environment
        self.service = service
        self.client = boto3.client('ssm', region_name=region)


    def get(self, key: str) -> str:
        return self.client.get_parameter(Name=f"/{self.environment}/{self.service}/{key}")['Parameter']['Value']