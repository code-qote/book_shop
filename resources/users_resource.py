from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Review, User, Book
from flask import jsonify
import datetime


def abort_404_user(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message='User not found')

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('image', required=False)
parser.add_argument('hashed_password', required=True)
parser.add_argument('basket', required=False)


class UserResource(Resource):
    def get(self, user_id):
        abort_404_user(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {'user':user.to_dict(only=('surname', 'name', 'email', 'image'))})
    
    def delete(self, user_id):
        abort_404_user(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})
    
class UserListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users':[user.to_dict(only=('surname', 'name', 'email', 'image')) for user in users]})
