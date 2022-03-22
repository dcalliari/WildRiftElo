import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime


load_dotenv(os.path.abspath('.env'))

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

ENV = os.environ.get('ENV')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = uri

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Broadcaster(db.Model):
    __tablename__ = 'broadcaster'
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(25), unique=True, nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    accounts = db.relationship("Account", backref="broadcaster")

# def __init__(self, twitch_id, accounts, created_at):
#     self.twitch_id = twitch_id
#     self.accounts = accounts
#     self.created_at = created_at


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    riot_id = db.Column(db.String(25))
    elo = db.Column(db.String(25))
    div = db.Column(db.Integer)
    pdl = db.Column(db.Integer)
    acc_id = db.Column(db.Integer, unique=True)
    broadcaster_id = db.Column(db.Integer, db.ForeignKey('broadcaster.id'))

    # def __init__(self, riot_id, elo, div, pdl):
    #     self.riot_id = riot_id
    #     self.elo = elo
    #     self.div = div
    #     self.pdl = pdl


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
