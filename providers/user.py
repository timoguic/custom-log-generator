import json
import random
from collections import namedtuple

from tqdm import tqdm

from ._ipv4 import IPv4Network
from .fields import make_field


class UserProvider:
    def __init__(self, config):
        """
        config is a massive dictionary (= config file loaded from yaml)
        It should be "sanitized".
        """
        if config.get("from_file"):
            self.load_from_file(config["from_file"])
        else:
            print("Generating users...")
            self.make_from_config(config["count"], **config["fields"])
            save_file = config.get("save_to")
            if save_file is not None:
                self.save(save_file)

    def make_from_config(self, count, **config_fields):
        fields = {}

        for field, config in config_fields.items():
            if config.get("generator") == "ipv4":
                self.ipv4_network = IPv4Network(
                    config["cidr_range"], config.get("excluded")
                )
                fields[field] = make_field(func=self.ipv4_network.get_ip_address)
            else:
                fields[field] = make_field(**config)

        user_klass = self.make_user_class(fields.keys())

        self.users = []
        for _ in tqdm(range(count)):
            mapping = {key: field.render() for key, field in fields.items()}
            self.users.append(user_klass(**mapping))

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as fp:
                data = json.load(fp)
        except json.JSONDecodeError:
            raise RuntimeError("Users file is invalid JSON.")

        if not len(data):
            raise RuntimeError("Users file seems to be empty.")

        if type(data) is not list:
            raise RuntimeError("Users file has an invalid format.")

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
