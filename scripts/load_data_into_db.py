# %%
from metadb import *
import json

# %% create all tables
all_models = BaseModel.__subclasses__()
with db:
    db.create_tables(all_models)

# %%
# load resource data
search_data_file = DATADIR / "metadata_from_search_results.json"
with open(search_data_file, "r", encoding="utf16") as f:
    search_data = json.load(f)

resource_data_file = DATADIR / "metadata_from_resource_pages.json"
with open(resource_data_file, "r", encoding="utf16") as f:
    resource_data = json.load(f)
    resource_data["authors"] = {tuple(json.loads(k)): v for k, v in resource_data["authors"].items()}

# %% fill metadata tables from source_data


def fill_table_id_name(Table, data):
    with db.atomic():
        Table.insert_many(
            [(k, v) for k, v in data.items()], fields=[Table.identifier, Table.name]
        ).execute()


def fill_table_name(Table, data):
    with db.atomic():
        Table.insert_many([(d,) for d in data], fields=[Table.name]).execute()


def fill_resource_relationship(Table, item_col, data, item_key):
    with db.atomic():
        for resource in data["resources"].values():
            for item in resource[item_key] or []:
                Table.create(resource=resource["identifier"], **{item_col: item})

def fill_resource_relationship(Table, item_col, data, item_key):
    with db.atomic():
        for resource in data["resources"].values():
            for item in resource.get(item_key) or []:
                Table.create(resource=resource["identifier"], **{item_col: item})

# %%

fill_table_id_name(Subject, search_data["subject"])
fill_table_id_name(MaterialType, search_data["material_type"])
fill_table_id_name(Provider, search_data["provider"])
fill_table_name(License, resource_data["license"])

# %% insert resource items
insert_keys = [
    "identifier",
    "title",
    "resource_page_url",
    "abstract",
    "date_added",
    "provider",
]
with db.atomic():
    for resource_id, row in search_data["resources"].items():
        row_data = {k: row[k] for k in insert_keys if k in row.keys()}
        if resource_id in resource_data:
            license_name = resource_data["resources"][resource_id]["license"]
            if license_name:
                row_data["license"] = license_name[0]
        Resource.create(**row_data)

# %% resource-subject relationships
fill_resource_relationship(ResourceSubject, "subject", search_data, "subject")
#  resource-type relationships
fill_resource_relationship(ResourceType, "type", search_data, "type")

# %% Tags
# fill tags table
fill_table_id_name(Tag, resource_data["tags"])
fill_resource_relationship(ResourceTag, "tag", resource_data, "tags")

# %% Level
fill_table_name(Level, resource_data["level"])
fill_resource_relationship(ResourceLevel, "level", resource_data, "level")
# %%
fill_table_name(Language, resource_data["language"])
fill_resource_relationship(ResourceLanguage, "language", resource_data, "language")
# %%
fill_table_name(Grade, resource_data["grades"])
fill_resource_relationship(ResourceGrade, "grade", resource_data, "grades")
# %%
fill_table_name(Format, resource_data["format"])
fill_resource_relationship(ResourceFormat, "format", resource_data, "format")
# %%
fill_table_name(Alignment, resource_data["alignment"])
fill_resource_relationship(ResourceAlignment, "alignment", resource_data, "alignment")
# %%
fill_table_name(Audience, resource_data["audience"])
fill_resource_relationship(ResourceAudience, "audience", resource_data, "audience")

# %% Authors
author_ids = {}
# set an integer primary key for each (author, href) combiantion
author_ids = {k: i for i, k in enumerate(resource_data["authors"].keys())}
with db.atomic():
    Author.insert_many(
        [
            (
                author_ids[(author, href)],
                author,
                href,
                resource_data["authors"][(author, href)],
            )
            for (author, href) in resource_data["authors"].keys()
        ],
        fields=[Author.identifier, Author.name, Author.href, Author.profile_id],
    ).execute()

# %% author - resource relationships
with db.atomic():
    for resource in resource_data["resources"].values():
        for i in range(len(resource.get("author",[]))):
            author_key = (resource["author"][i], resource["author_href"][i])
            author_id = author_ids[author_key]
            ResourceAuthor.create(resource=resource["identifier"], author=author_id)
