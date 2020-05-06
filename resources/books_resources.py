from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Book
from flask import jsonify



def abort_404(book_id):
    session = create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f'Book {book_id} not found') 


class BookResource(Resource):
    def get(self, book_id):
        abort_404(book_id)
        session = create_session()
        book = session.query(Book).get(book_id)
        return jsonify(
            {'book':book.to_dict(only=('name', 'about', 'author', 'year', 'genre', 'price', 'is_new', 'is_bestseller', 'image'))})

class BookListResource(Resource):
    def get(self):
        session = create_session()
        books = session.query(Book).all()
        return jsonify({'books': [book.to_dict(
            only=('name', 'about', 'author', 'year', 'genre', 'price', 'is_new', 'is_bestseller', 'image')) for book in books]})
