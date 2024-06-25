# %%
import json
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup as BSoup

from project import DATADIR

# %% load articles from search scrape
with open(DATADIR / 'search_results.json', "r", encoding="utf16") as f:
    articles_html = json.load(f)
    articles_soup = {
        identifier: BSoup(article, "lxml")
        for identifier, article in articles_html.items()
    }
    
# %% Process all articles
subject = {}
materialtype = {}
provider = {}
resources = {}

for resource_id, html_article in articles_soup.items():
    resource = {}
    resource["identifier"] = resource_id
    for link in html_article.find_all("a", class_="item-link js-item-link"):
        resource["title"] = link.text
        resource["resource_page_url"] = link.get("href")
    # use full abstract if available, otherwise fall back to short
    abstract = html_article.find_all("div", class_="abstract-full")
    if len(abstract) == 0:
        abstract = html_article.find_all("div", class_="abstract-short")
    if len(abstract) == 0:
        resource["abstract"] = None
    else:
        resource["abstract"] = abstract[0].get_text().strip()

    metadata = html_article.find_all(
        "dl", class_="item-info visible-md-block visible-lg-block"
    )[0]

    # extract dd's
    meta_dd = defaultdict(list)
    current_dt = None
    for meta in metadata.children:
        if meta.name == "dt":
            current_dt = meta.get_text()
            continue
        if meta.name == "dd":
            meta_dd[current_dt].append(meta)

    resource["subject"] = []
    for dd in meta_dd["Subject:"]:
        a = dd.find_all("a")[0]
        identifier = a.get("href").split("=")[1]
        if identifier not in subject:
            subject[identifier] = a.get_text()
        resource["subject"].append(identifier)

    for dd in meta_dd["Date Added:"]:
        resource["date_added"] = dd.get_text()

    resource["type"] = []
    for dd in meta_dd["Material Type:"]:
        a = dd.find_all("a")[0]
        identifier = a.get("href").split("=")[1]
        if identifier not in materialtype:
            materialtype[identifier] = a.get_text()
        resource["type"].append(identifier)

    for dd in meta_dd["Provider:"]:
        a = dd.find_all("a")[0]
        identifier = a.get("href").split("=")[1]
        if identifier not in provider:
            provider[identifier] = a.get_text()
        resource["provider"] = identifier

    resources[resource_id] = resource

# %%
search_data = {}
search_data["resources"] = resources
search_data["subject"] = subject
search_data["material_type"] = materialtype
search_data["provider"] = provider

search_data_file = DATADIR / "metadata_from_search_results.json"

with open(search_data_file, "w", encoding="utf16") as f:
    json.dump(search_data, f, indent=2)
