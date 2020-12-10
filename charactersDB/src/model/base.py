'''
Created on 28 nov. 2020

@author: inilog
'''
from peewee import Model, CharField, TextField, IntegerField, ForeignKeyField
from peewee import SqliteDatabase


db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Status(BaseModel):
    name = CharField()
    description = TextField()


class Option(BaseModel):
    name = CharField()
    value = CharField()


class Element(BaseModel):
    status = ForeignKeyField(Status)
    URI = CharField(unique=True, null=True)


class Character(Element):
    name = CharField()
    summary = TextField()


class RelationType(Element):
    name = CharField()
    max_number_element = IntegerField()


class AttributeType(Element):
    name = CharField()
    summary = TextField()


class Attribute(Element):
    object = ForeignKeyField(Element)
    attribute_type = ForeignKeyField(AttributeType)
    value = TextField()


class Relation(Element):
    relation_type = ForeignKeyField(RelationType)

    #TODO: correct add element for replacement of many to many field.
    def add_element(self, new_element):
        if (len(self.characters) <= self.relation_type.max_number_element
                or self.relation_type.max_number_element == 0):
            self.elements.append(new_element)


class RelationElements(Element):
    relation = ForeignKeyField(Relation)
    element = ForeignKeyField(Element)


class DataBase(object):
    def __init__(self):
        self._db = db
        self._base_URI = None
        self._default_status = None
        
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
        status = [{'name':'ébauche',
                   'description': 'élément en cours d''ébauche'},
                  {'name':'validé',
                   'description': 'élément dont l''idée à été validé'},
                  {'name':'intégré', 'description':
        'élément dont l''idée à été intégré à une oeuvre'},
                  ]
        for i, new_status in enumerate(status):
            new_status_element = Status()
            new_status_element.name = new_status['name']
            new_status_element.description = new_status['description']
            new_status_element.save()
            if i == 0:
                self._default_status = new_status_element
                Option(name="default status",
                       value=str(new_status_element.id)).save()

    def load(self, file_name):
        self._db.init(file_name)
        self._db.connect()
        self._base_URI = Option.get(Option.name=="base_URI")
        id_default = int(Option.get(Option.name=="default status").value)
        self._default_status = Status.get(id=id_default)

    @property
    def base_URI(self):
        if self._base_URI is None:
            return None
        else:
            return self._base_URI.value

    @property
    def default_status(self):
        return self._default_status


table_db = [Status, Option, Character, RelationType, Relation, AttributeType,
            Attribute, RelationElements]
