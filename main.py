from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from flask import redirect
from flask_wtf.csrf import CsrfProtect
from wtforms import *
from wtforms.validators import DataRequired
from flask import render_template
from data import db_session
from data.__all_models import *
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from resources import books_resources, reviews_resources, genres_resources, users_resource
from forms import *
import datetime
from werkzeug.utils import secure_filename
from requests import get, post, delete
from email.mime.text import MIMEText
from email.header import Header
import smtplib
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

def send_email(email, text):
    smtp_host = 'smtp.yandex.ru'
    login, password = 'bshelf.shop@yandex.ru', 'password_to_app'

    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = Header('Заказ', 'utf-8')
    msg['From'] = login
    msg['To'] = email
    sender = smtplib.SMTP(smtp_host, 587)
    sender.set_debuglevel(1)
    sender.starttls()
    sender.login(login, password)
    try:
        sender.sendmail(
        msg['From'], msg['To'], msg.as_string())
    except:
        return 'Error'


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
            name=form.name.data,
            basket=''
        )
        if form.image.data:
            tp = secure_filename(form.image.data.filename)[-4:]
            filename = form.email.data + tp
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
@app.route('/new', methods=['GET', 'POST'])
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

@app.route('/genres/<int:genre_id>', methods=['GET', 'POST'])
def genre_page(genre_id):
    search = SearchForm()
    
    books = list(filter(lambda x: x['genre'] == genre_id, get(url_api + '/books').json()['books']))
    genres = get(url_api + '/genres').json()['genres']
    return render_template('main_page.html', books=main_page_books(books), genres=genres, search=search)

@app.route('/bestsellers', methods=['GET', 'POST'])
def bestsellers_page():
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
    books = list(filter(lambda x: x['is_bestseller'] == 1, get(url_api + '/books').json()['books']))
    genres = get(url_api + '/genres').json()['genres']
    return render_template('main_page.html',  books=main_page_books(books), genres=genres, search=search)

@app.route('/books/<int:book_id>', methods=['GET', 'POST'])
def book_page(book_id):
    search = SearchForm()
    review = ReviewForm()
    buying = BuyingForm()
    buying.check_count(book_id)
    ordered = False
    if current_user.is_authenticated and current_user.basket:
        basket = current_user.basket
        basket = [i.split() for i in basket.split(',')][:-1]
        for i in basket:
            if int(i[0]) == book_id:
                ordered = True
                break
    if search.validate_on_submit():
        books = get(url_api + '/books').json()['books']
        request = search.request.data
        for book in books:
            book['search'] = len(set(request.split()) & set(f"{book['name']} {book['author']} {book['year']} {book['price']}".split()))
        books.sort(key = lambda x: x['search'])
        books = list(filter(lambda x: x['search'] != 0, books))
        genres = get(url_api + '/genres').json()['genres']
        return render_template('main_page.html', books=main_page_books(books), genres=genres, search=search)
    if buying.validate_on_submit():
        session = create_session()
        book = session.query(Book).get(book_id)
        user = session.query(User).get(current_user.id)
        user.basket += f'{book_id} {buying.count.data},'
        book.count -= buying.count.data
        session.commit()
        return redirect('/books/' + str(book_id))
    book = get(url_api + '/books/' + str(book_id)).json()['book']
    reviews = get(url_api + '/reviews').json()['reviews']
    users = get(url_api + '/users').json()['users']
    accepted = True
    if list(filter(lambda x: x['author'] == current_user.id and x['book'] == book_id, reviews)):
        accepted = False
    reviews = list(filter(lambda x: x['book'] == book_id, reviews))
    if review.validate_on_submit():
        json = {
            'author': current_user.id,
            'rate': review.rating.data,
            'text': review.text.data,
            'book': book_id,
            'user': f'{current_user.name} {current_user.surname}',
        }
        if current_user.image:
            json['image'] = current_user.image
        post(url_api + '/reviews', json=json)
        reviews = get(url_api + '/reviews').json()['reviews']
        reviews = list(filter(lambda x: x['book'] == book_id, reviews))
        accepted = False
        return render_template('book_page.html', book=book, accepted=accepted, ordered=ordered, reviews=reviews, search=search, review=review, buying=buying)
    return render_template('book_page.html', book=book, accepted=accepted, ordered=ordered, reviews=reviews, search=search, review=review, buying=buying)     
    
@app.route('/basket/<int:user_id>', methods=['GET', 'POST'])
@login_required
def basket_page(user_id):
    form = BasketForm()
    search = SearchForm()
    session = create_session()
    text = ''
    basket = [i.split() for i in current_user.basket.split(',')][:-1]
    books = get(url_api + '/books').json()['books']
    items = []
    total = 0
    for item in basket:
        book = list(filter(lambda x: x['id'] == int(item[0]), books))[0]
        text += f"{ book['name'] } { book['author'] } { item[1] } \n{int(item[1]) * book['price']} руб.\n-------------------\n"
        items.append(
            {
                'id': book['id'],
                'name': book['name'],
                'author': book['author'],
                'count': int(item[1]),
                'price': book['price']
            }
        )
        total += book['price'] * int(item[1])
    text += f'Итого: {total}'
    if search.validate_on_submit():
        books = get(url_api + '/books').json()['books']
        request = search.request.data
        for book in books:
            book['search'] = len(set(request.split()) & set(f"{book['name']} {book['author']} {book['year']} {book['price']}".split()))
        books.sort(key = lambda x: x['search'])
        books = list(filter(lambda x: x['search'] != 0, books))
        genres = get(url_api + '/genres').json()['genres']
        return render_template('main_page.html', books=main_page_books(books), genres=genres, search=search)
    if form.validate_on_submit():
        user = session.query(User).get(current_user.id)
        send_email(user.email, text)
        user.basket = ''
        session.commit()
        return redirect('/')
    return render_template('basket_page.html', items=items, total=total, form=form, search=search)       
    
@app.route('/delete_review/<int:book_id>/<int:review_id>', methods=['GET', 'DELETE'])
def delete_review(book_id, review_id):
    delete(url_api + '/reviews/' + str(review_id))
    return redirect(f'/books/{book_id}')

@app.route('/delete_basket_item/<int:user_id>/<int:book_id>', methods=['GET', 'POST'])
def delete_basket_item(user_id, book_id):
    session = create_session()
    basket = [i.split() for i in current_user.basket.split(',')][:-1]
    for item in basket.copy():
        if int(item[0]) == book_id:
            basket.remove(item)
            break
    user = session.query(User).get(user_id)
    user.basket = ','.join([' '.join(item) for item in basket])
    session.commit()
    return redirect('/basket/' + str(user_id))

def main():
    db_session.global_init("db/database.sqlite")
    api.add_resource(books_resources.BookResource, '/api/books/<int:book_id>')
    api.add_resource(books_resources.BookListResource, '/api/books')
    api.add_resource(reviews_resources.ReviewResource, '/api/reviews/<int:review_id>')
    api.add_resource(reviews_resources.ReviewListResource, '/api/reviews')
    api.add_resource(genres_resources.GenreResource, '/api/genres/<int:genre_id>')
    api.add_resource(genres_resources.GenreListResource, '/api/genres')
    api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
    api.add_resource(users_resource.UserListResource, '/api/users')
    app.run(port=8080, host='127.0.0.1')
    csfr.init_app(app)


if __name__ == '__main__':
    main()
