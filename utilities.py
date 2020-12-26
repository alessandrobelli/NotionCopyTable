import sys
from uuid import uuid1
from copy import copy 
from notion.client import NotionClient
from notion.utils import extract_id
import os
from random import choice

colors = [
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
]


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def _find_prop_schema(schema, prop):
    return next((v for k, v in schema.items() if v["name"] == prop), None)

def _add_new_multi_select_value(collection, prop, value, color=None):
    if color is None:
        color = choice(colors)

    schema = collection.get("schema")
    prop_schema = _find_prop_schema(schema,prop)


    if not prop_schema:
        raise ValueError(
            f'"{prop}" property does not exist on the collection!'
        )

    if not "options" in prop_schema:
        prop_schema["options"] = []

    dupe = next(
        (o for o in prop_schema["options"] if o["value"] == value), None
    )
    if not dupe:
        prop_schema["options"].append(
        {"id": str(uuid1()), "value": value, "color": color}
        )
        try:
            collection.set("schema", schema)
        except (RecursionError, UnicodeEncodeError):
        # Catch `RecursionError` and `UnicodeEncodeError`
        # in `notion-py/store.py/run_local_operation`,
        # because I've no idea why does it raise an error.
        # The schema is correctly updated on remote.
            pass    

