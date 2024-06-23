
# Working with OER Commons metadata

## OER Commons

[OER Commons](https://oercommons.org/) is a databased of open educational resources. You can browse around the website and play with the search to get an idea of how it works. You can [browse](https://oercommons.org/oer) by subject area and material type. You can also browse by [provider](https://oercommons.org/oer/providers).

We have scraped a database of metadata of the OER commons items. This 

## Possible tasks

- What can we learn about the coverage of OER Commons from this metadata? E.g. visualizing coverage according to level, language, tags (ie location). This could include word clouds of tags, visualizations of resources by location, charting the growth of the data base over time (every item has a date added), looking at resources across levels in different languages.
  
- In addition to static infographics and plots, could consider a dashboard for users to interactively query the database. 
  
- How can we use AI tools to validate or improve this metadata? Can we learn more from embeddings of the descriptions (allowing semantic search, or automatic tag generation based on clustering descriptions).

### Python environment

- We suggest using `conda` from Miniconda or [Miniforge](https://github.com/conda-forge/miniforge). If you have this installed you can create a conda enviroment for this project with `conda env create -f environment.yml`, then activate it with `conda activate oer-scraping`. 
- If something goes wrong with the environment and you need to recreate it from scratch you can do this with `conda env create -f environment.yml --yes`.

### Data

- We have extracted metadata for all the items in OER Commons. This data is available [here, in the Dropbox folder](CHANGELINK). Unzip the `data.zip` folder in this project, then you will to uncompress the 7zip archives. You can get [7zip for Windows here](https://www.7-zip.org/). For Mac you can use [Keka](https://www.keka.io/en/).
- `metadata_from_search_results.json` contains the metadata obtained from the search result listings. The `resources` entry is a dict with one value for each resource indentifier, which is a dict. This has keys with a signle value: `identifier`, `title`, `resource_page_url`, `abstract`, `provider`, and the following keys which store a list of multiple values: `subject`, and `type` (Material Type). The keys `subject`, `material_type` and `provider` provide dicts that contain all the possible values for that field seen across the data base and map between the indentifier (used as the value of the parameter in the URL of the search function) and the name (i.e. readable string with capitalisation and spaces).
- `metadata_from_resource_pages.json`  contains additional metadata obtained from the resource pages (but not including OERCommons hosted courseware). `resources` contains the metadata for each resource consisting of: `tags`, `level`, `language`, `format`, `grades`, `license`, 'license_href', `author`, `author_href`, `profile_id`, `audience`, `alignment`. The unique values for each of these are also stored. 
- This metadata is also available in an Sqlite DB, using the [`peewee`](https://docs.peewee-orm.com/en/latest/) ORM. The definition of the database is in [`src/db.py`](src/db.py).

- EXAMPLE Ipynb to get started. 