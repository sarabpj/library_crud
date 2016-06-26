from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/python_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    books = db.relationship('Book', backref='name', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # This is what will be displayed when you examine an instance
    def __repr__(self):
        return 'name {}'.format(self.name)

class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, title,author_id):
        self.title = title
        self.author_id = author_id

    # This is what will be displayed when you examine an instance
    def __repr__(self):
        return 'title {}'.format(self.title)

db.drop_all() # drop tables

db.create_all() # create tables

hm = Author('Herman Melville')
ad = Author('Alexander Dumas')

moby_dick = Book('Moby Dick', 1) # make a new instance/row
harry_potter = Book('Count of Monte Cristo', 2) # make a new instance/row
db.session.add(hm)
db.session.add(ad)
db.session.add(moby_dick)
db.session.add(harry_potter)

db.session.commit() 
from IPython import embed; embed()