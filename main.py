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
from resources import books_resources, reviews_resources
from forms import *
import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'scrtky'
csfr = CsrfProtect()


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
            form.image.data.save('tests/' + filename)
            with open('tests/' + filename, 'rb') as file:
                user.image = file.read()
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

@app.route('/')
def main_page():
    search = SearchForm()
    return render_template('main_page.html', search=search)


def main():
    db_session.global_init("db/database.sqlite")
    api.add_resource(books_resources.BookResource, '/api/books/<int:book_id>')
    api.add_resource(books_resources.BookListResource, '/api/books')
    api.add_resource(reviews_resources.ReviewResource, '/api/reviews/<int:review_id>')
    api.add_resource(reviews_resources.ReviewListResource, '/api/reviews')
    app.run(port=8080, host='127.0.0.1')
    csfr.init_app(app)


if __name__ == '__main__':
    main()
