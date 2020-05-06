from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from flask import redirect
from flask_wtf.csrf import CsrfProtect
from wtforms import *
from wtforms.validators import DataRequired
from flask import render_template, g
from data import db_session
from data.__all_models import *
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from resources import books_resources, reviews_resources, genres_resources
from forms import *
import datetime
from werkzeug.utils import secure_filename
from requests import get, post, delete
import os


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'scrtky'
csfr = CsrfProtect()
url_api = 'http://localhost:8080/api'


def main_page_books(books):
    new = []
    last = 0
    for i in range(len(books)):
        if i % 3 == 0 and i != 0:
            new.append(books[i - 3:i])
            last = i
    if len(books) % 3 != 0:
        new.append(books[-(len(books) - last):])
    return new


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой Email уже используется")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save('static/users/' + filename)
            user.image = filename
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Email или пароль не совпадают",
                               form=form)
    return render_template('login.html', title='Вход', form=form)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    search = SearchForm()
    if search.validate_on_submit():
        books = get(url_api + '/books').json()['books']
        request = search.request.data
        for book in books:
            book['search'] = len(set(request.split()) & set(f"{book['name']} {book['author']} {book['year']} {book['price']}".split()))
        books.sort(key = lambda x: x['search'])
        books = list(filter(lambda x: x['search'] != 0, books))
        genres = get(url_api + '/genres').json()['genres']
        return render_template('main_page.html', books=main_page_books(books), genres=genres, search=search)
    books = list(filter(lambda x: x['is_new'] == 1, get(url_api + '/books').json()['books']))
    genres = get(url_api + '/genres').json()['genres']
    return render_template('main_page.html',  books=main_page_books(books), genres=genres, search=search)

@app.route('/genres/<int:genre_id>')
def genre_page(genre_id):
    search = SearchForm()
    books = list(filter(lambda x: x['genre'] == genre_id, get(url_api + '/books').json()['books']))
    genres = get(url_api + '/genres').json()['genres']
    return render_template('main_page.html', books=main_page_books(books), genres=genres, search=search)

@app.route('/books/<int:book_id>')
def book_page(book_id):
    search = SearchForm()
    


def main():
    db_session.global_init("db/database.sqlite")
    api.add_resource(books_resources.BookResource, '/api/books/<int:book_id>')
    api.add_resource(books_resources.BookListResource, '/api/books')
    api.add_resource(reviews_resources.ReviewResource, '/api/reviews/<int:review_id>')
    api.add_resource(reviews_resources.ReviewListResource, '/api/reviews')
    api.add_resource(genres_resources.GenreResource, '/api/genres/<int:genre_id>')
    api.add_resource(genres_resources.GenreListResource, '/api/genres')
    app.run(port=8080, host='127.0.0.1')
    csfr.init_app(app)


if __name__ == '__main__':
    main()
