from logging import getLogger
from pathlib import Path
from string import Template

import yaml

log = getLogger(__name__)


def check_for_pattern(data):
    if "pattern" not in data.keys():
        raise KeyError("No `pattern` in the config file.")


def check_users(data):
    if "users" in data:
        if "count" not in data["users"]:
            raise KeyError("No `count` defined for the user provider.")

        if "fields" not in data:
            raise KeyError("No `fields` defined for the user provider.")

    if "users_file" in data:
        if "users" in data:
            raise KeyError("Cannot define users AND import users.")

        if not Path(data["users_file"]).is_file():
            raise KeyError(f"Users file {data['users_file']} does not exist.")


def check_fields(data):
    try:
        p = Template(data["pattern"])
        mapping = {name: "" for name in data["fields"].keys()}
        p.substitute(**mapping)
    except KeyError:
        raise KeyError("The pattern and fields don't match.")


def check_config(data):
    validators = [check_for_pattern, check_fields, check_users]

    for func in validators:
        func(data)


def load_config(yaml_file):
    with open(yaml_file, "r") as f:
        log.debug(f"Loading file {yaml_file}")
        data = yaml.load(f, Loader=yaml.FullLoader)

        check_config(data)

        return data
