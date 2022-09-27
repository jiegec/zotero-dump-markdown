from collections import defaultdict
import sqlite3
import os
from markdownify import markdownify as md

db = sqlite3.connect(f"{os.getenv('HOME')}/Zotero/zotero.sqlite")

# Fetch all papers
data = db.execute(
    """
select I.itemID, f.fieldName, DV.value from itemNotes N
    inner join items I on I.itemID = N.parentItemID
    inner join itemData D on I.itemID = D.itemID
    inner join fields f on D.fieldID = f.fieldID
    inner join itemDataValues DV on D.valueID = DV.valueID
;
"""
)

items = defaultdict(dict)
for (id, key, value) in data:
    items[id][key] = value

# Fetch all notes
data = db.execute(
    """
select I.itemID, N.note from itemNotes N
    inner join items I on I.itemID = N.parentItemID
;
"""
)

for (id, note) in data:
    items[id]["note"] = note

items = list(sorted(items.values(), key=lambda i: i["title"]))
for props in items:
    title = props["title"]
    print(f"## {title}")
    print()

    for k in props:
        if k in ["date", "DOI", "proceedingsTitle", "url", "publicationTitle"]:
            print(f"{k}: {props[k]}")

    # Convert html to markdown
    print()
    print(md(props["note"]).strip())

    print()
