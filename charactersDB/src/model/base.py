'''
Created on 28 nov. 2020

@author: inilog
'''
from peewee import Model, CharField, TextField, ForeignKeyField, IntegerField
from peewee import SqliteDatabase, BooleanField


db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Universe(BaseModel):
    URI = CharField(unique=True)
    name = CharField(null=True)
    description = TextField(null=True)


class Status(BaseModel):
    name = CharField()
    description = TextField()


class Option(BaseModel):
    name = CharField()
    value = CharField()


class Element(BaseModel):
    status = ForeignKeyField(Status)
    universe = Universe(null=True)
    URI = CharField(unique=True, null=True)
    next_unic_URI_value = IntegerField(default=1)


class Work(Element):
    """ describe a work (book, scenary, film, ...) were an element occure
    linked by a relation with predicate
    """
    name = CharField()
    description = TextField()


class Character(Element):
    name = CharField()
    summary = TextField()


class Predicate(Element):
    name = CharField()
    create_subelement = BooleanField(default=False)
    is_subelement = BooleanField(default=False)


class Relation(Element):
    subject = ForeignKeyField(Element)
    predicate = ForeignKeyField(Element)
    object = ForeignKeyField(Element)


class AttributeType(Element):
    name = CharField()
    summary = TextField()


class Attribute(Element):
    subject = ForeignKeyField(Element)
    attribute_type = ForeignKeyField(AttributeType)
    value = TextField()


class DataBase(object):
    def __init__(self):
        self._db = db
        self._base_URI = None
        self._default_status = None
        self._version = 0
        
    def create(self, file_name, base_URI):
        if file_name[-3:] != '.cdb':
            file_name += '.cdb'
        self._db.init(file_name)
        self._db.connect()
        self._db.create_tables(table_db)
        if base_URI[-1:] != '/':
            base_URI += '/'
        self._base_URI = Option(name="base_URI", value=base_URI)
        self._base_URI.save()
        version = Option(name='version', value=self._version)
        version.save()
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


meta_table = [Element, Universe, Status, Option, Predicate, Relation,
              AttributeType, Attribute]
table_db = meta_table + [Character]
