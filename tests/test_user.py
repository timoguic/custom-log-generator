from unittest.mock import mock_open, patch

import pytest

from config import load_config
from providers import UserProvider

USERS_FROM_JSON = """---
users:
  from_file: userfile.json

timestamps:
  interval: 1

log_entries: 1
  
pattern: $name $browser
fields:
  name:
    provider: user
    attribute: name
  browser:
    provider: user
"""


def test_load_users_from_file(USERS_JSON):
    with patch("builtins.open", new_callable=mock_open, read_data=USERS_JSON):
        up = UserProvider({"from_file": "userfile.json"})

        assert len(up.users) == 1
        u = up.random_user
        assert u.name == "John Smith"
        assert u.user_agent == "Internet Explorer 4"


def test_generate_users():
    CONF = {
        "fields": {
            "something": {"provider": "static", "data": "Hello!"},
            "name": {"func": "name"},
        },
        "count": 10,
    }
    up = UserProvider(CONF)
    assert len(up.users) == 10
    assert hasattr(up.users[0], "name")
    assert up.users[0].something == "Hello!"


def test_load_from_file_invalid_json():
    with patch("builtins.open", new_callable=mock_open, read_data=""):
        with pytest.raises(RuntimeError):
            UserProvider({"from_file": "userfile.json"})


def test_load_from_file_empty_json():
    with patch("builtins.open", new_callable=mock_open, read_data="[]"):
        with pytest.raises(RuntimeError):
            UserProvider({"from_file": "empty.json"})


def test_load_from_file_empty_json():
    with patch("builtins.open", new_callable=mock_open, read_data="{}"):
        with pytest.raises(RuntimeError):
            UserProvider({"from_file": "empty.json"})
