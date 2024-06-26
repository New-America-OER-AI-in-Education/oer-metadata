# %%
from dotenv import load_dotenv

load_dotenv(override=True)

from openai import OpenAI
import numpy as np

# %%
test_strings = [
    "Students explore the interface between architecture and engineering. In the associated hands-on activity, students act as both architects and engineers by designing and building a small parking garage.",
    "test string 2",
]

# %%
model = "text-embedding-ada-002"
# can be:
# "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"

client = OpenAI()

embs = client.embeddings.create(input=test_strings, model=model)

# %%
embsarr = np.array([emb.embedding for emb in embs.data])

print(embsarr.shape)
