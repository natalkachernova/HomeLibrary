from flask import Flask, jsonify, abort, make_response, request, render_template
from models import bookslibrary

app = Flask(__name__)
app.config["SECRET_KEY"] = "booklib"


@app.route("/", methods=["GET"])
def homepage():   
  return render_template("base.html")

@app.route('/bookslist', methods=["GET"])
def bookslist():
  items = bookslibrary.all()
  return render_template("books_list.html", items=items)

@app.route('/booksissued', methods=["GET"])
def booksissued():
  items = bookslibrary.allissued()
  return render_template("books_issued.html", items=items)

@app.route("/bookinfo/<book_id>", methods=["GET"])
def getbook(book_id):
  bookdetails = bookslibrary.getbookinfo(book_id)
  name_button = "Hand out the book"
  if bookdetails[6]:
    name_button = "Return the book"
  if not bookdetails:
    abort(404)
  return render_template("bookinfo.html", namebook=bookdetails, name_button=name_button)

@app.route("/bookadd", methods=["POST"])
def addbook():
  return render_template("create.html")

@app.route("/adding", methods=["POST"])
def addingbook():
  data = request.form  
  namebook = data.get('namebook')
  author = data.get('author')
  yearbook = data.get('yearbook')
  description = data.get('description')
  coverimage = data.get('coverimage')
  bookslibrary.create(namebook, author, yearbook, description, coverimage)
  items = bookslibrary.all()
  return render_template("books_list.html", items=items)

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/deletebook/<int:book_id>", methods=['POST'])
def delete_book(book_id):
  result = bookslibrary.delete(book_id)
  if not result:
    abort(404)
  items = bookslibrary.all()
  return render_template("books_list.html", items=items)


@app.route("/changestatebook/<int:book_id>", methods=['POST'])
def update_book(book_id):
  bookslibrary.update(book_id)
  items = bookslibrary.all()
  return render_template("books_list.html", items=items)


@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
  app.run(debug=True)
