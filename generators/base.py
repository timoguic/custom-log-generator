import random

from faker import Faker

fake = Faker()


def name():
    return fake.name()


def from_file(filename=None):
    with open(filename, "r") as fp:
        return random.choice(fp.readlines()).strip()


def from_list(values=None):
    if not values:
        values = []
    return random.choice(values)


def randint(min=0, max=65535):
    return random.randint(min, max)
