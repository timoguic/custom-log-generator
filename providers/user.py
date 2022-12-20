import json
import logging
import random
from collections import namedtuple

from tqdm import tqdm

from ._ipv4 import IPv4Network
from .fields import make_field

logger = logging.getLogger("clg." + __name__)


class UserProvider:
    """Manages users and their attributes to inject in log entries"""

    def __init__(self, count=None, fields=None, from_file=None, save_to=None):
        if from_file:
            # Load users from an existing JSON file
            logger.debug(f"Loading users from file {from_file}")
            self.load_from_file(from_file)
        else:
            # Generate them
            self.make_from_config(count, **fields)
            if save_to is not None:
                self.save(save_to)

    def make_from_config(self, count, **config_fields):
        """Create `count` users based on the `config_fields`"""
        fields = {}

        for field, config in config_fields.items():
            if config.get("generator") == "ipv4":
                # Create a network, then use it in a field with a bound method :)
                self.ipv4_network = IPv4Network(config["cidr_range"], config.get("excluded"))
                fields[field] = make_field(func=self.ipv4_network.get_ip_address)
            else:
                fields[field] = make_field(**config)

        # Dynamically create a class to represent this user configuration
        user_klass = self.make_user_class(fields.keys())

        self.users = []

        logger.debug(f"Generating {count} users...")

        for _ in tqdm(range(count)):
            mapping = {key: field.render() for key, field in fields.items()}
            self.users.append(user_klass(**mapping))

    def load_from_file(self, filename):
        """Load the users from an existing JSON file.
        We assume the fields are consistent across all users."""
        try:
            with open(filename, "r") as fp:
                data = json.load(fp)
        except json.JSONDecodeError:
            raise RuntimeError("Users file is invalid JSON.")

        if not len(data):
            raise RuntimeError("Users file seems to be empty.")

        if type(data) is not list:
            raise RuntimeError("Users file has an invalid format.")

        # We will use the first user fields to create the User class...
        first = data[0]
        user_klass = self.make_user_class(first.keys())
        self.users = [user_klass(**elem) for elem in data]

    @property
    def random_user(self):
        return random.choice(self.users)

    @staticmethod
    def make_user_class(fields):
        return namedtuple("User", fields)

    def save(self, filename):
        with open(filename, "w") as fp:
            json.dump([u._asdict() for u in self.users], fp)

        logger.debug(f"Users saved to {filename}.")
