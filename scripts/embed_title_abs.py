# %%
from dotenv import load_dotenv
load_dotenv(override=True)
import json
from openai import OpenAI
import numpy as np
from project import DATADIR
from tqdm import tqdm


#%%
# load strings to embed
with open(DATADIR / "strings_to_embed.json", 'r') as f:
    embed_strings = json.load(f)

#%%
num_strings = len(embed_strings)
# %%
model = "text-embedding-3-small"
# can be:
# "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"
client = OpenAI()
resource_embeddings = {}
#%%
import itertools
def chunked(it, size):
    it = iter(it)
    while True:
        p = tuple(itertools.islice(it, size))
        if not p:
            break
        yield p

# for k,v in tqdm(embed_strings.items()):
batch_size = 2000
i = 0
for chunk in chunked(embed_strings.keys(), batch_size):
    print("chunk: ",i)
    i = i + 1
    strings = [embed_strings[k] for k in chunk]
    embs = client.embeddings.create(input=strings, model=model)
    for k,v in zip(chunk, embs.data):
        resource_embeddings[k] = v

#%%
resource_embs_np = {k, np.array(v.embedding)}
np.array([emb.embedding for emb in embs.data])