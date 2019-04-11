import feedparser
from datetime import datetime
from flask import Flask, request, Response, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import *
from config import Config

import os
import scrapy
from future import Future
import time
from time import mktime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)


title = "Scraping Flight deals"
heading = "Scraping Flight deals"

RSS_FEEDS = {
    'https://www.secretflying.com/posts/category/san-francisco/feed/',
    'https://www.secretflying.com/posts/category/oakland/feed/',
    # 'http://www.theflightdeal.com/category/flight-deals/SFO/feed/',
    'https://www.fly4free.com/flights/flight-deals/usa/feed?s=san+francisco',
    'https://airfarespot.com/category/north-america/san-francisco/feed/',
}

@app.route("/", methods=['GET', 'POST'])
def default():
    return get_news()

@app.route("/fetch")
def lists ():
    #Display the all Tasks
    os.system("scrapy crawl booking_crawler > booking_urls.csv")
    return title

@app.route("/list")
def deals ():
    #Display the all Tasks
    deals = Deal.query.order_by(Deal.pubdate.desc()).all()
    for deal in deals:
        print(deal)
    return render_template("list.html", deals=deals)

# @app.route("/wired")
# def wired():
#   return get_news('wired')

# @app.route("/bbc")
# def bbc():
#   return get_news('bbc')

def get_news():
    # pull down all feeds
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in RSS_FEEDS]
    # block until they are all in
    feeds = [future_obj() for future_obj in future_calls]

    entries = []
    for feed in feeds:
        entries.extend( feed[ "items" ] )
    for entry in entries:
        print(entry.summary)
        if Deal.query.filter_by(guid= entry["id"]).first():
            continue
        else:
            deal = Deal(entry["id"], entry["title"], entry["summary"], entry["link"], datetime.fromtimestamp(mktime(entry["published_parsed"])))
            db.session.add(deal)
            db.session.commit()
    sorted_entries = sorted(entries,reverse=True, key=lambda entry: entry["published_parsed"])
    # print(sorted_entries) # for most recent entries firsts

    return render_template("home.html", articles=sorted_entries)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
