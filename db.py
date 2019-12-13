"""Database models and database related functions."""

import os
from datetime import datetime

from peewee import (
    BlobField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    Model,
    TextField,
)

from config import DB, DB_FILE_PATH


class BaseModel(Model):
    """Model inherited by other database tables."""

    class Meta:
        database = DB


class Password(BaseModel):
    """DB table used to store password meta data for key pairs."""

    hint = TextField()
    strong = BooleanField()


class KeyPair(BaseModel):
    """DB table used to store asymmetric key pairs."""

    name = TextField(unique=True)
    public_key = BlobField()
    private_key = BlobField()
    password = ForeignKeyField(Password, backref="archives", null=True)
    timestamp = DateTimeField(default=datetime.now)


class Archive(BaseModel):
    """DB table used to store archive metadata."""

    name = TextField()
    src_path = TextField()
    dst_path = TextField()
    timestamp = DateTimeField(default=datetime.now)
    key_pair = ForeignKeyField(KeyPair, backref="archives")


def init_db(db_path):
    """Initializes the database.

    Args:
        db_path (str): The path where the database file will be created.
    """
    DB.init(db_path)
    DB.create_tables([Archive, KeyPair, Password])


def db_exists():
    """Checks if the database exists.

    Returns:
        bool: True if the database already exists, False otherwise.
    """
    return True if os.path.isfile(DB_FILE_PATH) else False
