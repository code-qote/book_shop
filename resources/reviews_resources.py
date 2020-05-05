from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Review
from flask import jsonify


def abort_404(review_id):
    session = create_session()
    review = session.query(Review).get(review_id)
    if not review:
        abort(404, message=f'Review {review_id} not found')

parser = reqparse.RequestParser()
parser.add_argument('author', required=True, type=int)
parser.add_argument('book', required=True)
parser.add_argument('date', required=True)


class ReviewResource(Resource):
    def get(self, review_id):
        abort_404(review_id)
        session = create_session()
        book = session.query(Review).get(review_id)
        return jsonify(
            {'review':book.to_dict(only=('author', 'book', 'date'))})

class ReviewListResource(Resource):
    def get(self):
        session = create_session()
        reviews = session.query(Review).all()
        return jsonify({'review':[review.to_dict(only=('author', 'book', 'date')) for review in reviews]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        review = Review(
            author=args['author'],
            book=args['book'],
            date=args['date']
        )
        session.add(review)
        session.commit()
        return jsonify({'success': 'OK'})
