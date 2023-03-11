from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, Text
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired

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


class BookLibraryForm(FlaskForm):
    namebook = StringField('namebook', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    yearbook = StringField('yearbook', validators=[DataRequired()])
    coverimage = StringField('coverimage', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    issued = BooleanField('issued', validators=[DataRequired()])
  
class BooksLibrary:
  def all(self):
    conn = engine.connect()
    sql = homelibrary.select().where(homelibrary.c.issued == False)
    result = conn.execute(sql)
    conn.close()
    return result

  #SELECT
  def allissued(self):
    conn = engine.connect()
    sql = homelibrary.select().where(homelibrary.c.issued == True)
    result = conn.execute(sql)
    conn.close()
    return result

  def getbookinfo(self, id):
    conn = engine.connect()
    sql = homelibrary.select().where(homelibrary.c.id == id)
    result = conn.execute(sql)
    row = result.fetchone()
    conn.close()
    return row

  #INSERT INTO
  def create(self, namebook, author, yearbook, description, coverimage):
    conn = engine.connect()
    sql = homelibrary.insert().values(namebook = namebook, 
                                      author = author,
                                      yearbook = yearbook,
                                      description = description,
                                      coverimage = coverimage,
                                      issued = False)
    result = conn.execute(sql, [{'namebook': namebook, 'author': author, 'yearbook': yearbook,
                                 'description': description,'coverimage': coverimage, 'issued': False}])
    conn.commit()
    conn.close()

  #DELETE
  def delete(self, id):
    book_id = self.getbookinfo(id)
    if book_id:
      conn = engine.connect()
      stmt = homelibrary.delete().where(homelibrary.c.id == id)
      conn.execute(stmt)
      conn.commit()
      conn.close()
      return True
    return False

  #UPDATE
  def update(self, id):
    book_id = self.getbookinfo(id)
    if book_id:
      conn = engine.connect()
      if book_id[6]:
        stmt=homelibrary.update().where(homelibrary.c.id==id).values(issued=False)
      else:
        stmt=homelibrary.update().where(homelibrary.c.id==id).values(issued=True)
      conn.execute(stmt)
      conn.commit()
      return True
    return False


bookslibrary = BooksLibrary()
