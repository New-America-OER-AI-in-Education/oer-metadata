# %%
from collections import defaultdict
from pathlib import Path
from itertools import product, chain
import json
import re

from joblib import Parallel, delayed
import requests
from bs4 import BeautifulSoup as BSoup
from tqdm import tqdm

from project import DATADIR

RESOURCECONTENTDIR = DATADIR / "resource_content"

# %%
# leave out courseware/ as it i
resource_files = [
    f
    for content_dir in [
        RESOURCECONTENTDIR / "authoring",
        RESOURCECONTENTDIR / "materials",
    ]
    for f in content_dir.rglob("*")
    if not f.is_dir() and not f.name[0] == "." and not f.name[-1] == "~"
]

resource_ids = [
    ".".join(file.relative_to(RESOURCECONTENTDIR).parts) for file in resource_files
]


def get_file_from_resource_id(resource_id):
    *id_folder, id_fname = resource_id.split(".")
    return RESOURCECONTENTDIR / "/".join(id_folder) / id_fname


def get_resource_id_from_file(file):
    return ".".join(file.relative_to(RESOURCECONTENTDIR).parts)


def get_text_from_html_csv(section):
    return [
        s.strip()
        for s in ("".join([x.get_text() for x in section.contents]).strip().split(","))
    ]


def get_text_from_links(section):
    return [x.get_text().strip() for x in section.find_all("a")]


def get_href_from_links(section):
    return [x.get("href") for x in section.find_all("a")]


# %%
tags = {}
resources = {}
resources_md = {}
authors = {}
observed_values = defaultdict(set)

for file in tqdm(resource_files):
    resource_id = get_resource_id_from_file(file)
    # if resource_id.startswith(("courseware.unit.", "courseware.courseware.")):
    #   continue
    resource = {}
    resource["identifier"] = resource_id
    with open(file, encoding="utf-16") as f:
        html = f.read()
    soup = BSoup(html, "lxml")

    # tags
    resource["tags"] = []
    tag_section = soup.find("section", **{"class": "item-tags"})
    if tag_section:
        tag_section = tag_section.find_all("a", **{"class": None})
        for tag in tag_section:
            tag_id = tag["href"].split("=")[-1]
            if tag_id not in tags:
                tags[tag_id] = tag.text
            resource["tags"].append(tag_id)

    # resource_url
    url = soup.find(
        "a", class_="view-resource-link btn btn-primary js-save-search-parameters"
    )
    resource["resource_url"] = url.get("href")

    # material details
    material_details = defaultdict()
    materials_parts = [
        soup.find("dl", class_="materials-details-first-part"),
        soup.find("div", class_="material-details-second-part"),
    ]
    for part in materials_parts:
        if part.name == "div":
            children = part.find_next("dl").children
        else:
            children = part.children
        for item in children:
            if item.name == "dt":
                current_dt = item.get_text()
                continue
            if item.name == "dd":
                material_details[current_dt] = item
    resources_md[resource_id] = material_details

    # mapping between section label and key name in database
    text_sections = {
        "Level:": "level",
        "Language:": "language",
        "Media Format:": "format",
        "Grades:": "grades",
    }
    # now parse the material_details
    for label, field in text_sections.items():
        if label in material_details:
            resource[field] = get_text_from_html_csv(material_details[label])
            observed_values[field].update(resource[field])
        else:
            resource[field] = None

    # license and author always have links, and we want to save those
    # for license, link has version which is not always in text
    # for author, f.browse search on name means no profile, others will have a profile link
    text_href_sections = {"License:": "license"}  # , "Author:": "author"}
    for label, field in text_href_sections.items():
        href_field = field + "_href"
        if label in material_details:
            resource[field] = get_text_from_links(material_details[label])
            observed_values[field].update(resource[field])
            resource[href_field] = get_href_from_links(material_details[label])
            observed_values[href_field].update(resource[href_field])
        else:
            resource[field] = None
            resource[href_field] = None

    # handle authors
    # not it seems there may be different links for the same author name, how to handle this?
    # extract author profile_id if present
    label = "Author:"
    if label in material_details:
        # if "profile" in author_href then save the number
        # print(material_details['Author:'])
        resource["author"] = get_text_from_links(material_details[label])
        resource["author_href"] = get_href_from_links(material_details[label])
        author_profiles = []
        resource["author_profile"] = []
        for url in resource["author_href"]:
            match = re.search(r"/profile/(\d+)", url)
            if match:
                profile_id = match.group(1)  # Return the numerical part
                resource["author_profile"].append(profile_id)
            else:
                resource["author_profile"].append(None)
        for author, href, profile_id in zip(
            resource["author"], resource["author_href"], resource["author_profile"]
        ):
            # use combination of text and href to index author as there are more
            # unique hrefs than there are unique name texts
            author_key = (author, href)
            if author_key not in authors:
                authors[author_key] = profile_id

    audience = []
    for role in soup.find_all("span", itemprop="educationalRole"):
        role_name = role.get_text()
        audience.append(role_name)
    if audience:
        observed_values["audience"].update(audience)
        resource["audience"] = audience

    alignment = []
    for link in soup.find_all("a", class_="alignment-tag-link"):
        alignment_id = link.get_text()
        alignment.append(alignment_id)
    if alignment:
        observed_values["alignment"].update(alignment)
        resource["alignment"] = alignment

    resources[resource_id] = resource

# %%

resource_data = {}
resource_data["resources"] = resources
resource_data["tags"] = tags
resource_data["authors"] = {json.dumps(k): v for k, v in authors.items()}



for field in observed_values.keys():
    resource_data[field] = list(observed_values[field])

resource_data_file = DATADIR / "metadata_from_resource_pages.json"

with open(resource_data_file, "w", encoding="utf16") as f:
    json.dump(resource_data, f, indent=2)


# %% save URLS separately for external scraping project
resource_url = {
    resource_id: resource["resource_url"] for resource_id, resource in resources.items()
}
with open(DATADIR / "resource_urls.json", "w", encoding="utf8") as f:
    json.dump(resource_url, f, indent=2)
