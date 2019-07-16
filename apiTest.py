from flask import Flask, jsonify, request, make_response
import re

app = Flask(__name__)

books = [
    {"ISBN":"978-1491918661", "Title":"Learning​ ​ PHP, MySQL​ ​ & JavaScript:​ ​ With jQuery,​​ CSS​ ​ & HTML5",
     "Author": "Robin Nixon", "Category": "PHP,​ Javascript", "Price": "9.99​ ​ GBP"},
    {"ISBN":"978-0596804848", "Title":"Ubuntu:​ Up​ and Running:​ A Power​ User's Desktop​ Guide",
     "Author": "Robin Nixon", "Category": "Linux", "Price": "12.99​ ​ GBP"},
    {"ISBN":"978-1118999875", "Title":"Linux​ Bible",
     "Author": "Christopher Negus", "Category": "Linux", "Price": "19.99​ ​ GBP"},
    {"ISBN":"978-0596517748", "Title":"JavaScript:​ The Good​ Parts",
     "Author": "Douglas Crockford", "Category": "JavaScript", "Price": "8.99 GBP"}
]

@app.route('/', methods=['GET'])
def getAllBooks():
    return jsonify({'books': books})

@app.route('/<string:key>/', methods=['GET'])
def getKey(key):
    #Shows a list of categories or authors. Duplicate listings removed.
    if key.lower() in ["author", "authors"]:
        return jsonify({"Authors" : list(dict.fromkeys([book["Author"] for book in books]))})
    if key.lower() in ["category", "categories"]:
        return jsonify({"Categories": list(dict.fromkeys([book["Category"] for book in books]))})

@app.route('/<string:key>/<string:value>', methods=['GET'])
#Shows a list of books from a certain author or category
def getBooks(key, value):
    if key.lower() in ["author", "authors"]:
        authorBooks = [book for book in books if book['Author'].lower() == value.lower()]
        return jsonify({'books': authorBooks})
    if key.lower() in ["category", "categories"]:
        categoryBooks = [book for book in books if book['Category'].lower() == value.lower()]
        return jsonify({'books': categoryBooks})

@app.route('/<string:key>/<string:value>/<string:addFilter>', methods=['GET'])
#Shows a list of books from a certain author or category and adds an extra filter by author or category.
def getBooksFilter(key, value, addFilter):
    if key.lower() in ["author", "authors"]:
        authorBooks = [book for book in books if book['Author'].lower() == value.lower()]
        filterBooks = [filterBook for filterBook in authorBooks if filterBook['Category'].lower() == addFilter.lower()]
        return jsonify({'books': filterBooks})
    if key.lower() in ["categories", "category"]:
        categoryBooks = [book for book in books if book['Category'].lower() == value.lower()]
        filterBooks = [filterBook for filterBook in categoryBooks if filterBook['Author'].lower() == addFilter.lower()]
        return jsonify({'books': filterBooks})


@app.route('/add/', methods=['POST', 'GET'])
def createBook():
    # Makes a wee form to add a new book
    if request.method == 'POST':
        if re.search('[a-zA-Z]', request.form.get("ISBN")): #Prevent ISBN from containing letters
            return make_response("Invalid ISBN", 400)
        newBook = {
         'Title': request.form.get('Title'),
         'ISBN': request.form.get("ISBN") ,
         "Author" : request.form.get("Author"),
         "Category": request.form.get("Category"),
         "Price" : request.form.get("Price")
         }

        books.append(newBook)
        return jsonify({'book': newBook}), 201

    return '''<form method="POST">
                  Title: <input type="text" name="Title"><br>
                  ISBN: <input type="text" name="ISBN"><br>
                  Author: <input type="text" name="Author"><br>
                  Category: <input type="text" name="Category"><br>
                  Price: <input type="text" name="Price"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    app.run()