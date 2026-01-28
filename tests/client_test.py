from pydoc import cli

import boto3
import pytest
from moto import mock_aws

from ps_client import ConfigClient


@mock_aws
def test_get():
    aws_client = boto3.client('ssm', region_name='us-east-1')
    aws_client.put_parameter(Name='/test/service/foo', Value='bar', Type='String')
    client = ConfigClient('test', 'service', 'us-east-1')
    assert client.get('foo') == 'bar'

@mock_aws
def test_missing_key():
    client = ConfigClient('test', 'service', 'us-east-1')
    with pytest.raises(KeyError, match=".*missing-key not found."):
        client.get('missing-key')

@mock_aws
def test_wrong_region():
    virginia, sydney = "us-east-1", "ap-southeast-2"
    aws_client = boto3.client('ssm', region_name=virginia)
    aws_client.put_parameter(Name='/test/service/foo', Value='bar', Type='String')
    # region mis-configured
    client = ConfigClient('test', 'service', sydney)
    assert virginia != sydney
    with pytest.raises(KeyError, match=".*foo not found."):
        client.get('foo')


@mock_aws
def test_get_secret():
    aws_client = boto3.client('ssm', region_name='us-east-1')
    aws_client.put_parameter(Name='/test/service/foo', Value='bar', Type='SecureString')
    client = ConfigClient('test', 'service', 'us-east-1')
    assert client.get_secret('foo') == 'bar'

@mock_aws
def test_attempt_get_secret_for_clear_text_parameter():
    aws_client = boto3.client('ssm', region_name='us-east-1')
    aws_client.put_parameter(Name='/test/service/foo', Value='bar', Type='String')
    client = ConfigClient('test', 'service', 'us-east-1')
    assert client.get_secret('foo') == 'bar'

@mock_aws
def test_attempt_get_for_cipher_text_parameter():
    aws_client = boto3.client('ssm', region_name='us-east-1')
    aws_client.put_parameter(Name='/test/service/foo', Value='bar', Type='SecureString')
    client = ConfigClient('test', 'service', 'us-east-1')
    with pytest.raises(ValueError, match=".*foo] is encrypted."):
        client.get('foo')
