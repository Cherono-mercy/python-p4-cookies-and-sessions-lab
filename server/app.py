#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    articles = []
    for article in Article.query.all():
        article_dict = article.to_dict()
        articles.append(article_dict) 

    response = make_response(
        jsonify(articles),
        200
    ) 

    return response   

@app.route('/articles/<int:id>')
def show_article(id):

#If this is the first request this user has made, set session["page_views"] to an initial value of zero using ternary operator
    session["page_views"] = session.get("page_views") or 0
    # For every request to '/articles/<int:id>' increment value of session["page_views"] by 1
    session["page_views"] += 1
    
    # If the user has viewed 3 pages or fewer, render a JSON response with the article data
    if session["page_views"] <= 3:
        article = Article.query.filter_by(id = id).first()
        article_dict = article.to_dict()

        response = make_response(
            jsonify(article_dict),
            200
        )
        return response
    
    # If the user has viewed more than 3 pages, return a JSON response including an error message and status code of 401 unauthorized
    return {"message": "Maximum pageview limit reached"}, 401


if __name__ == '__main__':
    app.run(port=5555)
