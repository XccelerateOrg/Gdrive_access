from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv, find_dotenv


class Base(DeclarativeBase):
    pass


_ = load_dotenv(find_dotenv("../.env"))

# declare SQLite DB and App
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = '962da5a46aa2aadd65d7bcaba821997ace8679jjj'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_DATABASE"]}'
db.init_app(app)

from gdrive_app import routes
