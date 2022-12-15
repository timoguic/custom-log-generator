from unittest.mock import mock_open, patch

from config import load_config
from providers import LogProvider

FULL_CONF = """---
users:
  count: 10
  fields:
    name:
      func: name
    user_agent:
      provider: static
      data: Safari

timestamps:
  start: 01-04-2010 12:42:05
  interval: 1

log_entries: 2
  
pattern: $time $name $browser
fields:
  time:
    provider: timestamp
    format: "%d/%m/%Y %H:%M:%S"
  name:
    provider: user
    attribute: name
  browser:
    provider: user
    attribute: user_agent

"""


def test_log_provider():
    with patch("builtins.open", new_callable=mock_open, read_data=FULL_CONF):
        conf = load_config("test.yaml")

    lp = LogProvider(conf)
    first_line = lp.generate()
    assert first_line.startswith("01/04/2010 12:42:05")
    assert first_line.endswith("Safari")
    assert lp.done is False

    second_line = lp.generate()
    assert second_line.startswith("01/04/2010 12:42:06")
    assert lp.done is True
