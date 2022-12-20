"""Base generators"""

import random

from faker import Faker

fake = Faker()


def name():
    """Wrapper for Faker.name"""
    return fake.name()


def from_file(filename=None):
    """Random line from file"""
    with open(filename, "r") as fp:
        return random.choice([line.strip() for line in fp])


def from_list(values=None):
    """Random element from list"""
    if not values:
        values = []
    return random.choice(values)


def randint(min=0, max=65535):
    """Wrapper for random.randint"""
    return random.randint(min, max)
