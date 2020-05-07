import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import *
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    basket = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    genre = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    is_new = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    is_bestseller = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                            primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    rate = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    book = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    