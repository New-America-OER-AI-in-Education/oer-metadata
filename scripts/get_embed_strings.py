# %%
from metadb import *
import json
import numpy as np
import matplotlib.pyplot as plt

# load resource data
search_data_file = DATADIR / "metadata_from_search_results.json"
with open(search_data_file, "r", encoding="utf16") as f:
    search_data = json.load(f)

resource_data_file = DATADIR / "metadata_from_resource_pages.json"
with open(resource_data_file, "r", encoding="utf16") as f:
    resource_data = json.load(f)
    resource_data["authors"] = {
        tuple(json.loads(k)): v for k, v in resource_data["authors"].items()
    }

# %%

lecture_notes = [
    r for r in search_data["resources"].values() if ("lecture-notes" in r["type"])
]
# embed_string = [r.get('title',"") + " " + r.get('abstract',"") for r in lecture_notes]
embed_string = {
    r["identifier"]: r["title"] + " " + r["abstract"]
    for r in lecture_notes
    if r["abstract"] is not None and r["title"] is not None
}

# %%
titles = {
    r["identifier"]: r["title"]
    for r in search_data["resources"].values()
    if r["abstract"] is not None
}

embed_strings = {
    k: v + " " + search_data["resources"][k]["abstract"]
    for k, v in titles.items()
    if search_data["resources"][k]["abstract"] is not None
}

#%% 
# how long are the strings we want to embed
# string_lengths = {k: len(v) for k,v in embed_strings.items()}
string_lengths = np.array(list({k: len(v) for k,v in embed_strings.items()}.values()))
long_strings = {k: v for k,v in embed_strings.items() if len(v)>10000}
plt.hist(string_lengths[string_lengths<5000])
# plt.hist(string_lengths)

# keep up to 3500 characters
# embed_strings = {k: v for k,v in embed_strings.items() if len(v)<3500}

#%% 
with open(DATADIR / "strings_to_embed.json",'w',encoding="utf8") as f:
    json.dump(embed_strings, f, indent=2)