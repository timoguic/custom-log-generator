from pathlib import Path

from .base import from_list

USER_AGENTS_PATH = Path(__file__).parent / "data" / "user_agents.txt"

with open(USER_AGENTS_PATH, "r") as fp:
    USER_AGENTS = fp.readlines()

DOMAINS_PATH = Path(__file__).parent / "data" / "domains.txt"
with open(DOMAINS_PATH, "r") as fp:
    DOMAINS = fp.readlines()

REQUESTS_URI_PATH = Path(__file__).parent / "data" / "requests.txt"
with open(REQUESTS_URI_PATH, "r") as fp:
    REQUESTS_URI = fp.readlines()


def user_agent():
    return from_list(USER_AGENTS).strip()


def domain():
    return from_list(DOMAINS).strip()


def request_uri():
    return from_list(REQUESTS_URI).strip()
