import pytest

from ps_client.client import get_key


def test_key():
    assert get_key("foo", "bar", "baz") == "/bar/baz/foo"


def test_assert_error_on_missing_service():
    with pytest.raises(ValueError, match="service is required."):
        get_key("foo", "bar", None)
