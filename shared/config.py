import logging
from copy import deepcopy
from json import dump, load
from os import environ as env
from os import path
from typing import Any

logging.info("Load configs")

if not path.exists("data/settings.json"):
    with open("data/settings.json", "w") as f:
        f.write("{}")
fields: dict[str, Any] = {
    "chances": {},
}

settings: dict[str, Any] = load(open("data/settings.json", "r"))
for key, default in fields.items():
    settings[key] = settings.get(key, deepcopy(default))


def save():
    dump(settings, open("data/settings.json", "w"))


# Configs
token = env["TOKEN"]
chances: dict[str, int] = settings["chances"]
