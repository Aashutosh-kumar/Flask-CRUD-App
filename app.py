from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Databse configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskreact'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)



#not to seee this msg

ma=Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.Text())
    date = db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,name,email):
        self.name=name
        self.email=email


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','date')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)




@app.route('/get',methods =['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route('/get/<id>',methods =['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)


@app.route('/update/<id>',methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    name = request.json['name']
    email = request.json['email']

    article.name = name
    article.email = email

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>',methods=['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/add',methods=['POST'])
def add_article():
    name = request.json['name']
    email = request.json['email']

    articles = Articles(name,email)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

if __name__=='__main__':
    app.run(debug=True)