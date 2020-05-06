from flask_restful import reqparse, abort, Api, Resource
from data.db_session import create_session
from data.__all_models import Genre
from flask import jsonify



def abort_404(genre_id):
    session = create_session()
    genre = session.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f'Genre {genre_id} not found') 


class GenreResource(Resource):
    def get(self, genre_id):
        abort_404(genre_id)
        session = create_session()
        genre = session.query(Genre).get(genre_id)
        return jsonify(
            {'genre':genre.to_dict(only=('name'))})

class GenreListResource(Resource):
    def get(self):
        session = create_session()
        genres = session.query(Genre).all()
        return jsonify({'genres': [genre.to_dict(
            only=('id', 'name')) for genre in genres]})
