
# Working with OER Commons metadata

## OER Commons

[OER Commons](https://oercommons.org/) is a databased of open educational resources. You can browse around the website and play with the search to get an idea of how it works. You can [browse](https://oercommons.org/oer) by subject area and material type. You can also browse by [provider](https://oercommons.org/oer/providers).

We have scraped a database of metadata of the OER commons items. This data is available both as raw Python (in json files), or imported into a relational database, using the [peewee](http://docs.peewee-orm.com/en/latest/) ORM. 

## Possible tasks

- What can we learn about the coverage of OER Commons from this metadata? E.g. visualizing coverage according to level, language, tags (i.e. location). This could include word clouds of tags, visualizations of resources by location, charting the growth of the data base over time (every item has a date added), looking at resources across levels in different languages.
  
- In addition to static infographics and plots, could consider a dashboard for users to interactively query the database.
  
- How can we use AI tools to validate or improve this metadata? Can we learn more from embeddings of the descriptions (allowing semantic search, or automatic tag generation based on clustering descriptions).

- Can we use AI to help us analyse the metadata? I.e. can you use LLMs to identify tags which refer to locations, so that statistics of the resources can be plotted on a map?

- Can we clean up or improve the database. At the moment the data is not perfectly clean. There are duplicate `tag_id`'s with the same text label. There maybe duplicate authors with the same name (but these might be different people). Resources with ids starting with `courseware.*` do not have their license info or tags added in the database.
  
- Extracting license information in a more robust way would be one area of improvement. We have saved the text and href of the license link from the webpage, but the same license text can have different links.

### Python environment

- We suggest using `conda` from Miniconda or [Miniforge](https://github.com/conda-forge/miniforge). If you have this installed you can create a conda enviroment for this project with `conda env create -f environment.yml`, then activate it with `conda activate oer-metadata`.
- If something goes wrong with the environment and you need to recreate it from scratch you can do this with `conda env create -f environment.yml --yes`.

### Data

- We have extracted metadata for all the items in OER Commons. This data is available [here, in the Dropbox folder](https://www.dropbox.com/scl/fi/jqqhk9b6tvhsco5e8gqig/data.zip?rlkey=alhqna4bbe2d1a5h3f8m7w6vq&dl=0). Unzip the `data.zip` folder in this project, then you will to uncompress the 7zip archives. You can get [7zip for Windows here](https://www.7-zip.org/). For Mac you can use [Keka](https://www.keka.io/en/).
- `metadata_from_search_results.json` contains the metadata obtained from the search result listings. The `resources` entry is a dict with one value for each resource indentifier, which is a dict. This has keys with a signle value: `identifier`, `title`, `resource_page_url`, `abstract`, `provider`, and the following keys which store a list of multiple values: `subject`, and `type` (Material Type). The keys `subject`, `material_type` and `provider` provide dicts that contain all the possible values for that field seen across the data base and map between the indentifier (used as the value of the parameter in the URL of the search function) and the name (i.e. readable string with capitalisation and spaces).
- `metadata_from_resource_pages.json`  contains additional metadata obtained from the resource pages (but not including OERCommons hosted courseware). `resources` contains the metadata for each resource consisting of: `tags`, `level`, `language`, `format`, `grades`, `license`, 'license_href', `author`, `audience`, `alignment`. The unique values for each of these are also stored. The `author` entry is a dict keyed by the tuple of (`author`, `author_href`), with the value as the `profile_id` extracted from the `author_href` if it contained one. 
- This metadata is also available in an Sqlite DB, using the [`peewee`](https://docs.peewee-orm.com/en/latest/) ORM. The definition of the database is in [`src/metadb.py`](src/metadb.py).
- You can load the raw data as:
```python
search_data_file = DATADIR / "metadata_from_search_results.json"
with open(search_data_file, "r", encoding="utf16") as f:
    search_data = json.load(f)

resource_data_file = DATADIR / "metadata_from_resource_pages.json"
with open(resource_data_file, "r", encoding="utf16") as f:
    resource_data = json.load(f)
    resource_data["authors"] = {tuple(json.loads(k)): v for k, v in resource_data["authors"].items()}
```
- To access the data through peewee:
```python
from metadb import *
query = (
    MaterialType.select(MaterialType, fn.Count(ResourceType.resource).alias("count"))
    .join(ResourceType)
    .group_by(MaterialType)
    .order_by(fn.Count(ResourceType.resource).desc())
)
q = pd.DataFrame(query.dicts())
q.head()
```
- You can also browse the [sqlite](https://www.sqlite.org/) database directly or use other SQL tools or ORMs. 
- You can see the database scheme in [`src/metadb.py`](src/metadb.py) and you can see how the data is loaded into the database in [`scripts/load_data_into_db.py`](scripts/load_data_into_db.py)
- You can see some further examples of working with the peewee database in [`scripts/example_queries.py`](scripts/example_queries.py)