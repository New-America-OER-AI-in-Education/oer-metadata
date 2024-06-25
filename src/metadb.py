import peewee as pw
from pathlib import Path
from peewee import fn

from project import DATADIR

DBFILE = DATADIR / "oercommons.db"

db = pw.SqliteDatabase(DBFILE)


class BaseModel(pw.Model):
    class Meta:
        database = db


class Subject(BaseModel):
    identifier = pw.CharField(primary_key=True)
    name = pw.CharField()


class MaterialType(BaseModel):
    identifier = pw.CharField(primary_key=True)
    name = pw.CharField(unique=True)


class Provider(BaseModel):
    identifier = pw.CharField(primary_key=True)
    name = pw.CharField(unique=True)


class License(BaseModel):
    name = pw.CharField(primary_key=True)


class Tag(BaseModel):
    identifier = pw.CharField(primary_key=True)
    # this should be unique, but it seems there are some duplicate tags with different ID
    # name = pw.CharField(unique=True)
    name = pw.CharField()


class Language(BaseModel):
    name = pw.CharField(primary_key=True)


class Level(BaseModel):
    name = pw.CharField(primary_key=True)


class Format(BaseModel):
    name = pw.CharField(primary_key=True)


class Grade(BaseModel):
    name = pw.CharField(primary_key=True)


class Audience(BaseModel):
    name = pw.CharField(primary_key=True)


class Alignment(BaseModel):
    name = pw.CharField(primary_key=True)


class Author(BaseModel):
    identifier = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    href = pw.CharField()
    profile_id = pw.IntegerField(null=True)

    class Meta:
        # impose uniqueness constraint on combination of name and href
        indexes = ((("name", "href"), True),)


class Resource(BaseModel):
    # from article item in search result
    identifier = pw.CharField(primary_key=True)
    title = pw.CharField()
    abstract = pw.CharField(null=True)
    date_added = pw.DateField(null=True)
    resource_page_url = pw.CharField()
    provider = pw.ForeignKeyField(Provider, backref="resources", null=True)
    license = pw.ForeignKeyField(License, backref="resources", null=True)


# many to many relationships
class ResourceType(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    type = pw.ForeignKeyField(MaterialType)

    class Meta:
        primary_key = pw.CompositeKey("resource", "type")


class ResourceSubject(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    subject = pw.ForeignKeyField(Subject)

    class Meta:
        primary_key = pw.CompositeKey("resource", "subject")


class ResourceTag(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    tag = pw.ForeignKeyField(Tag)

    class Meta:
        primary_key = pw.CompositeKey("resource", "tag")


class ResourceLevel(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    level = pw.ForeignKeyField(Level)

    class Meta:
        primary_key = pw.CompositeKey("resource", "level")


class ResourceGrade(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    grade = pw.ForeignKeyField(Grade)

    class Meta:
        primary_key = pw.CompositeKey("resource", "grade")


class ResourceFormat(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    format = pw.ForeignKeyField(Format)

    class Meta:
        primary_key = pw.CompositeKey("resource", "format")


class ResourceAudience(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    audience = pw.ForeignKeyField(Audience)

    class Meta:
        primary_key = pw.CompositeKey("resource", "audience")


class ResourceAlignment(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    alignment = pw.ForeignKeyField(Alignment)

    class Meta:
        primary_key = pw.CompositeKey("resource", "alignment")


class ResourceLanguage(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    language = pw.ForeignKeyField(Language)

    class Meta:
        primary_key = pw.CompositeKey("resource", "language")


class ResourceAuthor(BaseModel):
    resource = pw.ForeignKeyField(Resource)
    author = pw.ForeignKeyField(Author)

    class Meta:
        primary_key = pw.CompositeKey("resource", "author")
