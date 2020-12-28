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

    if isinstance(value,list):
        for vo in value:
            dupe = next(
                (o for o in prop_schema["options"] if o["value"] == vo), None
            )

            if not dupe:
                prop_schema["options"].append(
                {"id": str(uuid1()), "value": vo, "color": color}
                )
                try:
                    collection.set("schema", schema)
                except (RecursionError, UnicodeEncodeError):
                    print("error in setting schema")
                # Catch `RecursionError` and `UnicodeEncodeError`
                # in `notion-py/store.py/run_local_operation`,
                # because I've no idea why does it raise an error.
                # The schema is correctly updated on remote.
                    pass
    else:
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
                print("error in setting schema")
            # Catch `RecursionError` and `UnicodeEncodeError`
            # in `notion-py/store.py/run_local_operation`,
            # because I've no idea why does it raise an error.
            # The schema is correctly updated on remote.
                pass

def _build_selects(new_row,old_row):
    #check if any rows is a multi-select or select
    # and add values into it if not existing.
    new_schema = new_row.collection.get("schema")
    has_multi_select_or_select_1 = any(_find_prop_schema(new_schema, actual_prop := prop) and _find_prop_schema(new_schema, actual_prop := prop)["type"] in ["multi_select","select"] for prop in dir(new_row))
    has_multi_select_or_select_2 = any(_find_prop_schema(new_schema, actual_prop := prop.capitalize()) and _find_prop_schema(new_schema, actual_prop := prop.capitalize())["type"] in ["multi_select","select"] for prop in dir(new_row))
    array_of_selects = []
    if has_multi_select_or_select_1:
        print("\n1")
        while has_multi_select_or_select_1:
            if not checkKey(_find_prop_schema(new_schema, actual_prop),"options"):
                print("option not exist then dupe false")
                dupe = False
                _add_new_multi_select_value(new_row.collection,actual_prop,getattr(old_row,actual_prop))
            elif getattr(old_row,actual_prop):
                if isinstance(getattr(old_row,actual_prop),list):
                    for ov in getattr(old_row,actual_prop):   
                        print("it's a list and add each of -> "+ov)
                        dupe = next((o for o in _find_prop_schema(new_schema, actual_prop)["options"] if o["value"] in ov), None)
                        print("now print dupe ->")
                        print(dupe)
                        if not dupe:
                            print("not duplicate, creating")
                            _add_new_multi_select_value(new_row.collection,actual_prop,ov)
                else:
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
                    print(actual_prop)
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
                    dupe = next((o for o in _find_prop_schema(new_schema, actual_prop)["options"] if o["value"] in getattr(old_row,actual_prop)), None)
                    if not dupe:
                        print("not duplicate, creating")    
                        _add_new_multi_select_value(new_row.collection,actual_prop,getattr(old_row,actual_prop))
            array_of_selects.append(actual_prop)
            has_multi_select_or_select_1 = any(_find_prop_schema(new_schema, actual_prop := prop) and prop not in array_of_selects and _find_prop_schema(new_schema, actual_prop)["type"] in ["multi_select","select"] for prop in dir(new_row))
    elif has_multi_select_or_select_2:
        print("\n2")
        while has_multi_select_or_select_2:
            if not checkKey(_find_prop_schema(new_schema, actual_prop),"options"):
                print("option not exist then dupe false")
                dupe = False
                _add_new_multi_select_value(new_row.collection,actual_prop,getattr(old_row,actual_prop))
            elif getattr(old_row,actual_prop):
                if isinstance(getattr(old_row,actual_prop),list):
                    for ov in getattr(old_row,actual_prop):   
                        print("it's a list and add each of -> "+ov)
                        dupe = next((o for o in _find_prop_schema(new_schema, actual_prop)["options"] if o["value"] in ov), None)
                        print("now print dupe ->")
                        print(dupe)
                        if not dupe:
                            print("not duplicate, creating")
                            _add_new_multi_select_value(new_row.collection,actual_prop,ov)
                else:
                    dupe = next((o for o in _find_prop_schema(new_schema, actual_prop)["options"] if o["value"] in getattr(old_row,actual_prop)), None)
                    if not dupe:
                        print("not duplicate, creating")    
                        _add_new_multi_select_value(new_row.collection,actual_prop,getattr(old_row,actual_prop))
            array_of_selects.append(actual_prop)
            has_multi_select_or_select_2 = any(_find_prop_schema(new_schema, actual_prop := prop.capitalize()) and _find_prop_schema(new_schema, actual_prop := prop.capitalize())["type"] in ["multi_select","select"] for prop in dir(new_row))    

def checkKey(dict, key): 
    if key in dict.keys():
        return True
    else:
        return False

def is_list_of_strings(lst):
        return (bool(lst) and not isinstance(lst, str) and all(isinstance(elem, str) for elem in lst))
        # You could break it down into `if-else` constructs to make it clearer to read.