from flask import Flask, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from flask import redirect
from flask_wtf.csrf import CsrfProtect
from wtforms import *
from wtforms.validators import DataRequired
import flask_wtf.file
from flask import render_template

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторить пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    image = flask_wtf.file.FileField('Фотография', validators=[flask_wtf.file.FileRequired(), flask_wtf.file.FileAllowed(['jpg', 'png'], 'Только фотографии!')])
    sumbit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class SearchForm(FlaskForm):
    request = StringField('Введите запрос', validators=[DataRequired()])
    submit = SubmitField('Поиск')
