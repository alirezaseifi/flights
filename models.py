from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)


class Deal(db.Model):
    id = db.Column('deal_id', db.Integer, primary_key=True)
    guid = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String(60))
    description = db.Column(db.String)
    url = db.Column(db.String)
    parsed_url = db.Column(db.String)
    pubdate = db.Column(db.DateTime)
    price = db.Column(db.String)
    origin = db.Column(db.String)
    to = db.Column(db.String)
    alliance = db.Column(db.String)
    airline = db.Column(db.String)
    source = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.url = link
        self.pubdate = pubdate
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Deal Guid %r>' % (self.guid)

class BookingLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String(60))
    description = db.Column(db.String)
    url = db.Column(db.String)
    parsed_url = db.Column(db.String)
    pubdate = db.Column(db.DateTime)
    price = db.Column(db.String)
    origin = db.Column(db.String)
    to = db.Column(db.String)
    alliance = db.Column(db.String)
    airline = db.Column(db.String)
    source = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.url = link
        self.pubdate = pubdate
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Deal Guid %r>' % (self.guid)
