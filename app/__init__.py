from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('app.config.DevelopConfig')

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

from app.auth.views import auth

app.register_blueprint(auth)

from app.accounts.views import accounts

app.register_blueprint(accounts)


