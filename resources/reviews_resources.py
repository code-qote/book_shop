from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Review, User, Book
from flask import jsonify
import datetime


def abort_404_review(review_id):
    session = create_session()
    review = session.query(Review).get(review_id)
    if not review:
        abort(404, message='Review not found')

def abort_404_author(author_id):
    session = create_session()
    user = session.query(User).get(author_id)
    if not user:
        abort(404, message='User not found')

def abort_404_book(book_id):
    session = create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message='Book not found')


parser = reqparse.RequestParser()
parser.add_argument('author', required=True, type=int)
parser.add_argument('book', required=True, type=int)
parser.add_argument('rate', required=True, type=float)
parser.add_argument('text', required=False)
parser.add_argument('user', required=True)
parser.add_argument('image', required=False)


class ReviewResource(Resource):
    def get(self, review_id):
        abort_404_review(review_id)
        session = create_session()
        book = session.query(Review).get(review_id)
        return jsonify(
            {'review':book.to_dict(only=('author', 'rate', 'text', 'book', 'date', 'user', 'image'))})
    
    def delete(self, review_id):
        abort_404_review(review_id)
        session = create_session()
        review = session.query(Review).get(review_id)
        session.delete(review)
        session.commit()
        return jsonify({'success': 'OK'})

class ReviewListResource(Resource):
    def get(self):
        session = create_session()
        reviews = session.query(Review).all()
        return jsonify({'reviews':[review.to_dict(only=('id', 'author', 'rate', 'text', 'book', 'date', 'user', 'image')) for review in reviews]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        review = Review(
            author=args['author'],
            book=args['book'],
            date=str(datetime.datetime.now()),
            text=args['text'],
            rate=args['rate'],
            user=args['user'],
            image=args['image']
        )
        abort_404_author(args['author'])
        abort_404_book(args['book'])
        session.add(review)
        session.commit()
        return jsonify({'success': 'OK'})

