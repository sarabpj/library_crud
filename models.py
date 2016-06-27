from shared import db

class Author(db.Model):

    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    books = db.relationship('Book', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'id:{} name: {}'.format(self.id, self.name)



class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    tags = db.relationship('Tag', secondary='book_tags', backref=db.backref('books', lazy='dynamic'))

    def __init__(self, title,author_id):
        self.title = title
        self.author_id = author_id

    # This is what will be displayed when you examine in the python console
    def __repr__(self):
        return 'id: {}, title: {}, author_id: {}'.format(self.id, self.title, self.author_id)

class Tag(db.Model):
    __tablename__ = 'tags'

    id= db.Column(db.Integer, primary_key=True)
    genre= db.Column(db.Text())

    def __init__(self, genre):
        self.genre = genre

    def __repr__(self):
        return 'id:{} genre: {}'.format(self.id, self.genre)


book_tags = db.Table('book_tags',

    db.Column('id', db.Integer, primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'))

)