from shared import db

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
        return 'id: {}, title: {}, author_id: {}'.format(self.id, self.title, self.author_id)


# from IPython import embed; embed()