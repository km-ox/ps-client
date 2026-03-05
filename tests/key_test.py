from ps_client.client import get_key


def test_key():
    assert get_key("foo", "bar", "baz") == "/bar/baz/foo"
