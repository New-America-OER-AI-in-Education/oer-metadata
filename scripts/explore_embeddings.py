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
Xtsne = model.fit_transform(resource_embs)

#%%
# pca
model = PCA(n_components=2, random_state=0)
Xpca = model.fit_transform(resource_embs)

#%%
f,ax = plt.subplots()
ax.scatter(Xtsne[:,0], Xtsne[:,1], s=1, alpha=0.1)
# i = 4726
# ax.plot(Xtsne[i,0],Xtsne[i,1],'k',markersize=12)
#%% weird cluster
idx = np.logical_and((Xpca[:,0]>0.45), (Xpca[:,1]>0.2))
cluster_ids = [resource_ids[i] for i in np.where(idx)[0]]

#%%
#[i for i,x in enumerate(resource_ids) if x == "materials.course.146489"]

#%%
f,ax = plt.subplots()
ax.scatter(Xtsne[:,0], Xtsne[:,1], s=1, alpha=0.1)
# i = 4726

#%%
from sklearn.cluster import KMeans
mdl = KMeans(n_clusters=20)
mdl.fit(resource_embs)

#%%
f,ax = plt.subplots()
# ax.scatter(Xtsne[:,0], Xtsne[:,1], s=1, alpha=0.1)
ax.scatter(Xtsne[:,0], Xtsne[:, 1], c=mdl.labels_.astype(float), s=4, alpha=0.1)