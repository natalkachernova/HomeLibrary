from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, Text
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired

engine = create_engine('sqlite:///homelibrary.db')
conn = engine.connect()
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
    sql = homelibrary.select().where(homelibrary.c.issued == False)
    result = conn.execute(sql)
    return result

  #SELECT
  def allissued(self):
    sql = homelibrary.select().where(homelibrary.c.issued == True)
    result = conn.execute(sql)
    return result

  def getbookinfo(self, id):
    sql = homelibrary.select().where(homelibrary.c.id == id)
    result = conn.execute(sql)
    row = result.fetchone()
    return row

  #INSERT INTO
  def create(self, namebook, author, yearbook, description, coverimage):
    sql = homelibrary.insert().values(namebook = namebook, 
                                      author = author,
                                      yearbook = yearbook,
                                      description = description,
                                      coverimage = coverimage,
                                      issued = False)
    result = conn.execute(sql, [{'namebook': namebook, 'author': author, 'yearbook': yearbook,
                                 'description': description,'coverimage': coverimage, 'issued': False}])
    conn.commit()

  #DELETE
  def delete(self, id):
    book_id = self.getbookinfo(id)
    if book_id:
      stmt = homelibrary.delete().where(homelibrary.c.id == id)
      conn.execute(stmt)
      conn.commit()
      return True
    return False

  #UPDATE
  def update(self, id):
    book_id = self.getbookinfo(id)
    if book_id:

      if book_id[6]:
        stmt=homelibrary.update().where(homelibrary.c.id==id).values(issued=False)
      else:
        stmt=homelibrary.update().where(homelibrary.c.id==id).values(issued=True)
      conn.execute(stmt)
      conn.commit()

      return True
    return False

  def __del__(self):
    conn.close()


bookslibrary = BooksLibrary()
