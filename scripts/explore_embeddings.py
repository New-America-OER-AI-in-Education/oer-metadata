#%%
import numpy as np
import json
from project import DATADIR
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
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
# tsne
model = TSNE(n_components=2, random_state=0)
model.fit_transform(resource_embs[:5000,:])

#%%
# pca
model = PCA(n_components=2, random_state=0)
Xpca = model.fit_transform(resource_embs)

#%%
plt.scatter(Xpca[:,0], Xpca[:,1], s=1, alpha=0.1)

#%% weird cluster
idx = np.logical_and((Xpca[:,0]>0.45), (Xpca[:,1]>0.2))
cluster_ids = [resource_ids[i] for i in np.where(idx)[0]]
