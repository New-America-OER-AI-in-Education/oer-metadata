# %%
from metadb import *
import pandas as pd
import seaborn as sns

# %% Count how many resources are "lesson"'s
query = (
    ResourceType.select(fn.COUNT(ResourceType.resource).alias("count"))
    .join(MaterialType)
    .where(MaterialType.identifier == "lesson")
)
q = pd.DataFrame(query.dicts())
q.head()
# %% show all material types
query = (
    MaterialType.select(MaterialType, fn.Count(ResourceType.resource).alias("count"))
    .join(ResourceType)
    .group_by(MaterialType)
    .order_by(fn.Count(ResourceType.resource).desc())
)
q = pd.DataFrame(query.dicts())
q.head()
# %% show subjects
query = (
    Subject.select(Subject, fn.Count(ResourceSubject.resource).alias("count"))
    .join(ResourceSubject)
    .group_by(Subject.identifier)
    .order_by(fn.Count(ResourceSubject.resource).desc())
)

q = pd.DataFrame(query.dicts())
q.head()

# %% show languages
query = (
    Language.select(Language, fn.Count(ResourceLanguage.resource).alias("count"))
    .join(ResourceLanguage)
    .group_by(Language.name)
    .order_by(fn.Count(ResourceLanguage.resource).desc())
)

q = pd.DataFrame(query.dicts())
print(q)

# %% show formats
query = (
    Format.select(Format, fn.Count(ResourceFormat.resource).alias("count"))
    .join(ResourceFormat)
    .group_by(Format.name)
    .order_by(fn.Count(ResourceFormat.resource).desc())
)

q = pd.DataFrame(query.dicts())
print(q)

# %% show formats by languages
query = (
    Format.select(
        Format.name.alias("format"),
        Language.name.alias("language"),
        fn.COUNT(Resource.identifier).alias("resource_count"),
    )
    .join(ResourceFormat)  # Joins Format to ResourceFormat
    .join(
        Resource, on=(ResourceFormat.resource == Resource.identifier)
    )  # Joins ResourceFormat to Resource
    .switch(
        Resource
    )  # Necessary to change the join context back to Resource for the next join
    .join(ResourceLanguage)  # Joins Resource to ResourceLanguage
    .join(
        Language, on=(ResourceLanguage.language == Language.name)
    )  # Joins ResourceLanguage to Language
    .group_by(Format.name, Language.name)  # Groups by both Format and Language
    .order_by(fn.COUNT(Resource.identifier).desc())  # Orders by Format and Language
)
q = pd.DataFrame(query.dicts())
print(q.iloc[:15,:])
