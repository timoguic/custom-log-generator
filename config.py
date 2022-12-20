from logging import getLogger
from pathlib import Path
from string import Template

import yaml

logger = getLogger("clg." + __name__)


def check_for_pattern(data):
    if "pattern" not in data.keys():
        raise KeyError("No `pattern` in the config file.")


def check_users(data):
    """Check the users section of the config file"""
    if "users" not in data:
        return

    if "from_file" not in data["users"]:
        if "count" not in data["users"]:
            raise KeyError("No `count` defined for the user provider.")

        if "fields" not in data["users"]:
            raise KeyError("No `fields` defined for the user provider.")


def check_fields(data):
    """Check that the pattern and field match"""
    try:
        p = Template(data["pattern"])
        mapping = {name: "" for name in data["fields"].keys()}
        p.substitute(**mapping)
    except KeyError:
        raise KeyError("The pattern and fields don't match.")


def check_timestamp(data):
    """Check the timestamps section of the config file"""
    if "timestamps" not in data:
        raise KeyError("No `timestamps` configuration set.")

    if "office_hours" in data["timestamps"]:
        hours = data["timestamps"]["office_hours"]
        if not hours.get("start") or not hours.get("end"):
            raise KeyError("Must define `start` and `end` for office hours.")

        if hours["start"] >= hours["end"]:
            raise ValueError("Office hours start must be strictly less than end.")

        for val in hours["start"], hours["end"]:
            if not 0 <= val <= 24:
                raise ValueError("Office hours start and end must be between 0 and 24.")


def load_config(yaml_file):
    """Read the configuration file and validates it"""
    with open(yaml_file, "r") as f:
        logger.debug(f"Loading config from {yaml_file}.")
        data = yaml.load(f, Loader=yaml.FullLoader)

        validators = [check_for_pattern, check_fields, check_users, check_timestamp]

        for func in validators:
            func(data)

        logger.debug("Config file seems fine.")

        return data
