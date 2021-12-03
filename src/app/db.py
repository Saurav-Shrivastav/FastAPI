import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    ForeignKey,
    Boolean,
    create_engine
)
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(10), unique=True),
    Column("password", String(255)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
notifs = Table(
    "notifs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("user", ForeignKey("users.id")),
    Column("read_status", Boolean, unique=False, default=False),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
