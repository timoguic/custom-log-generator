from unittest.mock import mock_open, patch

import pytest

from config import load_config

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


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_PATTERN)
def test_config_no_pattern(mock_file):
    with pytest.raises(KeyError):
        load_config("empty.yaml")


@patch("builtins.open", new_callable=mock_open, read_data=MISSING_FIELDS)
def test_config_missing_fields(mock_file):
    with pytest.raises(KeyError):
        load_config("missing.yaml")
