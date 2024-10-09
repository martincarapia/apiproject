from flask import Flask, request, jsonify, render_template
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.as_dict() for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.as_dict())


@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.json
    book = Book(book_name=new_book['book_name'], 
                author=new_book['author'], 
                publisher=new_book.get('publisher')
                )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.as_dict()), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    updated_data = request.get_json()
    book.book_name = updated_data['book_name']
    book.author = updated_data['author']
    book.publisher = updated_data.get('publisher')
    db.session.commit()
    return jsonify(book.as_dict())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': "Book deleted"})

if __name__ == '__main__':
    app.run(debug=True)