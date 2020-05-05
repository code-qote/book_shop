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
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


class ReviewResource(Resource):
    def get(self, review_id):
        abort_404(review_id)
        session = create_session()
        book = session.query(Review).get(review_id)
        return jsonify(
            {'review':book.to_dict(only=('id', 'author', 'book', 'date'))})
    
    def post(self):


class ReviewListResource(Resource):
