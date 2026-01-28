import boto3
from moto import mock_aws

from ps_client import ConfigClient


@mock_aws
def test_get():
    aws_client = boto3.client('ssm', region_name='us-east-1')
    aws_client.put_parameter(Name='/test/test-service/test-key', Value='test-value', Type='String')
    client = ConfigClient('test', 'test-service', 'us-east-1')
    assert client.get('test-key') == 'test-value'