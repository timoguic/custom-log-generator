import pytest


@pytest.fixture
def USERS_FROM_JSON():
    return """---
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
    attribute: user_agent
"""


@pytest.fixture
def USERS_JSON():
    return """[
    {
        "name": "John Smith",
        "user_agent": "Internet Explorer 4"
    }
]"""
