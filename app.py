import os

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from quart import Quart, render_template
from dotenv import load_dotenv
from datetime import datetime


load_dotenv(os.path.abspath('.env'))

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

ENV = os.environ.get('ENV')

app = Quart(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Broadcaster(Base):
    __tablename__ = 'broadcaster'
    id = Column(Integer, primary_key=True)
    twitch_id = Column(String(25), unique=True, nullable=False)
    created_at = Column(Date, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    accounts = relationship("Account", backref="broadcaster")
    lang = Column(String(25), default="en")


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    hash = Column(String(25))
    acc_id = Column(Integer)
    broadcaster_id = Column(Integer, ForeignKey('broadcaster.id'))
    cache = Column(String(100))
    region = Column(String(3), default="na")


@app.route("/", methods=["GET"])
async def index():
    await render_template("index.html")


if __name__ == "__main__":
    app.run()
