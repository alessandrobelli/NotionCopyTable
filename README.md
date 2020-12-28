# NotionCopyTable

This script extend Notion allowing to copy rows with relationship.

## BEFORE YOU USE!

**Please test it in dummy tables before using on important ones, you might lose your data!**

1. Add in the destination table the columns you need to copy from the source table, with the same name.

### Known Issues

* you need to remove any column that has special char or spaces. For example change in both tables "How was it?" in "howwasit", then you can edit it again.
* check duplicates was tested only on a text (Title) field.

 
## How to use
Execute:

`python .\copy_tables.py`

then enter the required informations.
