import sys
import os
from notion.client import NotionClient
from copy import copy
from utilities import query_yes_no
from utilities import _find_prop_schema
from utilities import _add_new_multi_select_value
from termcolor import colored, cprint
import getpass
from tqdm import tqdm

# Notion Section
# 1 enter token
# 2 enter table to copy from
# 3 enter table to copy to
cprint("Welcome to Notion Copy-Rows!", 'white','on_grey', attrs=['bold'])

wants_to_check_duplicates = query_yes_no(
    "Do you want to check for duplicates?")

wants_to_remove_old_rows = query_yes_no(
    "Do you want to remove old rows?")

token = getpass.getpass("Enter your token_v2 (input hidden)\n")
client = NotionClient(token_v2=token)

url_from = input("Enter the link of the table you want to copy from \n")

table_from = client.get_collection_view(url_from)

url_to = input("Enter the link of the table you want to copy to \n")
table_to = client.get_collection_view(url_to)

if wants_to_check_duplicates:
    property_duplicates_from = input("Enter a valid name present in " +
                                table_from.collection.name+"\nCASE SENSITIVE PROPERTY NAME=")
    schema = table_from.collection.get("schema")
    prop_schema = _find_prop_schema(schema, property_duplicates_from)
    if not prop_schema:
        raise ValueError(
            f'"{property_duplicates_from}" property does not exist on the collection!'
        )    
    property_duplicates_to = input("Enter a valid name present in " +
                                table_to.collection.name+"\nCASE SENSITIVE PROPERTY NAME=")
    schema = table_to.collection.get("schema")
    prop_schema = _find_prop_schema(schema, property_duplicates_to)
    if not prop_schema:
        raise ValueError(
            f'"{property_duplicates_to}" property does not exist on the collection!'
        )



def _copy_properties(old, new):
    for prop in dir(old):
        try:
            if not prop.startswith('_'):
                attr = getattr(old, prop)
                schema = new.collection.get("schema")
                prop_schema_1 = _find_prop_schema(schema,prop)
                prop_schema_2 = _find_prop_schema(schema,prop.capitalize())
                if prop_schema_1 and (prop_schema_1["type"] == "multi_select" or prop_schema_1["type"] == "select") or prop_schema_2 and (prop_schema_2["type"] == "multi_select" or prop_schema_2["type"] == "select"):
                    _add_new_multi_select_value(new.collection, prop, attr)
                if attr != '' and not callable(attr):
                    setattr(new, prop, copy(attr))
        except AttributeError:
            pass
    if bool(old.children):
        for old_child in old.children:
            new_child = new.children.add_new(old_child.__class__)
            _copy_properties(old_child, new_child)


rows_table_from = table_from.build_query().execute()
iterator = 1
cprint("STARTING TO COPY!", 'white','on_grey', attrs=['bold','blink'])

for old_row in tqdm(rows_table_from):
    if wants_to_check_duplicates:
        table_query = table_to.default_query().execute()
        value_exists_already = any(getattr(x,property_duplicates_to) == getattr(old_row,property_duplicates_from) for x in table_query)
        if not value_exists_already:
            new_row = table_to.collection.add_row(bool(False))
            _copy_properties(old_row, new_row)
            iterator +=1
    else:
        new_row = table_to.collection.add_row(bool(False))
        _copy_properties(old_row, new_row)
    if wants_to_remove_old_rows:
        old_row.remove()

print("Copy Ended! \n")