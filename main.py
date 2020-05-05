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
import datetime


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'scrtky'
csfr = CsrfProtect()


def main():
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')
    csfr.init_app(app)


if __name__ == '__main__':
    main()
