from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from flask import redirect
from flask_wtf.csrf import CsrfProtect
from wtforms import *
from wtforms.validators import DataRequired, Email
import flask_wtf.file
from flask_wtf.html5 import NumberInput
from flask import render_template
from data.db_session import create_session
from data.__all_models import Book

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторить пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    image = flask_wtf.file.FileField('Фотография', validators=[flask_wtf.file.FileRequired(), flask_wtf.file.FileAllowed(['jpg', 'png'], 'Только фотографии!')])
    sumbit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class SearchForm(FlaskForm):
    request = StringField('Введите запрос', validators=[DataRequired()])
    submit = SubmitField('Поиск')

class ReviewForm(FlaskForm):
    text = TextAreaField('Ваш отзыв', validators=[DataRequired()])
    rating = IntegerField('Рейтинг', validators=[DataRequired()], widget=NumberInput(min=0, max=5, step=1))
    submit = SubmitField('Отправить')

class BuyingForm(FlaskForm):
    count = IntegerField('Количество', validators=[DataRequired()], widget=NumberInput())
    submit = SubmitField('Отправить в корзину')

    def check_count(self, id):
        session = create_session()
        book = session.query(Book).get(id)
        self.count.widget = NumberInput(min=1, max=book.count)

class BasketForm(FlaskForm):
    submit = SubmitField('Купить')
