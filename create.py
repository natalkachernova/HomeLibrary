from sqlalchemy import Table, Column, Integer, String, MetaData, Text, Boolean
from sqlalchemy import create_engine

engine = create_engine('sqlite:///homelibrary.db')

meta = MetaData()

homelibrary = Table(
   'homelibrary', meta,
    Column('id', Integer, primary_key=True),
    Column('namebook', String),
    Column('author', String),
    Column('yearbook', Integer),
    Column('coverimage', String),
    Column('description', Text),
    Column('issued', Boolean),
)

meta.create_all(engine)
