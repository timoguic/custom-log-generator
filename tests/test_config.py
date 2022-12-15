from unittest.mock import mock_open, patch

import pytest

from config import load_config
from providers import LogProvider, UserProvider

MISSING_PATTERN = """---
users:
fields:
"""

MISSING_FIELDS = """---
pattern: "$name $hello"
fields:
  name:
    generator: random
"""

USER_NAME_PATTERN = """
pattern: $name
fields:
  name:
    provider: user
    attribute: name
"""

MISSING_USER_COUNT = (
    """---
users:
  fields:
    name:
      func: name
"""
    + USER_NAME_PATTERN
)

MISSING_USER_FIELDS = (
    """---
users:
  count: 10
"""
    + USER_NAME_PATTERN
)


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_PATTERN)
def test_config_no_pattern(mock_file):
    with pytest.raises(KeyError):
        load_config("empty.yaml")


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_FIELDS)
def test_config_missing_fields(mock_file):
    with pytest.raises(KeyError):
        load_config("missing.yaml")


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_USER_COUNT)
def test_config_missing_user_count(mock_file):
    with pytest.raises(KeyError):
        load_config("missing_count.yaml")


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_USER_FIELDS)
def test_config_missing_user_fields(mock_file):
    with pytest.raises(KeyError):
        load_config("missing_user_fields.yaml")
