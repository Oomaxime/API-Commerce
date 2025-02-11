from flask import Flask, render_template, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)
is_logged_in = False

books = [
    {"id": 1, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "year": 1997},
    {"id": 2, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 4, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 5, "title": "A Promised Land", "author": "Barack Obama", "year": 2020}
]


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'admin':
        access_token = create_access_token(identity=username)
        response = make_response(render_template('index.html'))
        response.set_cookie('access_token', access_token)
        return response
    return "error"


@app.route('/')
def index():
    access_token = request.cookies.get('access_token')
    print(access_token)
    if access_token:
        return render_template('index.html', books=books)
    return render_template('login.html')

@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('search')
    if not query:
        return render_template('index.html', books=[], error="Please enter a search term.")
    
    matching_books = [book for book in books if query.lower() in book['author'].lower()]
    if not matching_books:
        return render_template('index.html', books=[], error="No books found matching your search.")
    
    return render_template('index.html', books=matching_books)

@app.route('/addBook', methods=['POST'])
def addBook():
    title = request.form.get('title')
    author = request.form.get('author')
    year = request.form.get('year')
    
    new_book = {
        'id': len(books) + 1,
        'title': title,
        'author': author,
        'year': int(year) if year else None
    }
    
    books.append(new_book)
    
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)