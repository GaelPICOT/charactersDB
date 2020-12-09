'''
Created on 28 nov. 2020

@author: inilog
'''
from peewee import Model, CharField, TextField, IntegerField, ForeignKeyField
from peewee import ManyToManyField, BooleanField, SqliteDatabase


db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Option(BaseModel):
    name = CharField()
    value = CharField()


class Element(BaseModel):
    validate = BooleanField(default=False)
    URI = CharField(unique=True, null=True)


class Character(Element):
    name = CharField()
    summary = TextField()


class RelationType(Element):
    name = CharField()
    max_number_character = IntegerField()


class RelationCharacter(Element):
    relation_type = ForeignKeyField(RelationType)
    characters = ManyToManyField(Character)

    def add_character(self, new_character):
        if (len(self.characters) <= self.relation_type.max_number_character
                or self.relation_type.max_number_character == 0):
            self.characters.append(new_character)


class AttributeType(Element):
    name = CharField()
    summary = TextField()


class Attribute(Element):
    object = ForeignKeyField(Element)
    attribute_type = ForeignKeyField(AttributeType)
    value = TextField()


class DataBase(object):
    def __init__(self):
        self._db = db
        
    def create(self, file_name, base_URI):
        if file_name[-3:] != '.cdb':
            file_name += '.cdb'
        self._db.init(file_name)
        self._db.connect()
        self._db.create_tables(table_db)
        if base_URI[-1:] != '/':
            base_URI += '/'
        self._base_URI = Option(name="base_URI", value = base_URI)
        self._base_URI.save()

    def load(self, file_name):
        self._db.init(file_name)
        self._db.connect()
        self._base_URI = Option.get(Option.name=="base_URI")

    @property
    def base_URI(self):
        if self._base_URI is None:
            return None
        else:
            return self._base_URI.value


table_db = [Option, Character, RelationType, RelationCharacter, AttributeType,
            Attribute]
