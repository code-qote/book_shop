from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Book
from flask import jsonify



def abort_404(book_id):
    session = create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f'Book {book_id} not found')

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('author', required=True)
parser.add_argument('year', required=True, type=int)
parser.add_argument('genre', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('is_new', required=True, type=bool)
parser.add_argument('is_bestseller', required=True, type=bool)
parser.add_argument('image', required=True)
parser.add_argument('count', required=True, type=int)


class BookResource(Resource):
    def get(self, book_id):
        abort_404(book_id)
        session = create_session()
        book = session.query(Book).get(book_id)
        return jsonify(
            {'book':book.to_dict(only=('name', 'about', 'author', 'year', 'genre', 'price', 'count', 'is_new', 'is_bestseller', 'image'))})
        
    def delete(self, book_id):
        abort_404(book_id)
        session = create_session()
        book = session.query(Book).get(book_id)
        session.delete(book)
        session.commit()
        return jsonify({'success': 'OK'})

class BookListResource(Resource):
    def get(self):
        session = create_session()
        books = session.query(Book).all()
        return jsonify({'books': [book.to_dict(
            only=('id', 'name', 'about', 'author', 'year', 'genre', 'price', 'count', 'is_new', 'is_bestseller', 'image')) for book in books]})
    
    def post(self):
        args = parser.parse_args()
        session = create_session()
        book = Book(
            name=args['name'],
            about=args['about'],
            author=args['author'],
            year=args['year'],
            genre=args['genre'],
            price=args['price'],
            is_new=args['is_new'],
            is_bestseller=args['is_bestseller'],
            image=args['image'],
            count=args['count']
        )
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})

