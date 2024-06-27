#%%
import numpy as np
import json
from project import DATADIR

#%%
with open(DATADIR / "embs_ids.json",'r',encoding="utf8") as f:
    resource_ids = json.load(f)
resource_embs = np.load(DATADIR / 'embs_array.npy')

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
#%%