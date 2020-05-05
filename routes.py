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
from main import login_manager, app, api


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
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Такой Email уже используется")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Register', form=form)

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
                               message="РќРµРїСЂР°РІРёР»СЊРЅС‹Р№ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ",
                               form=form)
    return render_template('login.html', title='РђРІС‚РѕСЂРёР·Р°С†РёСЏ', form=form)