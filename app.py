from flask import Flask, render_template, request, redirect, url_for
from models.shared import db
from models.author import Author
from models.book import Book
# Flask - class used to initialize an app
# render_template - render a template
# request - getting form data via POST request
# redirect - respond with location header
# url_for - shorthand for using function name instead of name of route

from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/library_in_class'


# Modus - allows us to do method override via headers or query string
# with ?_method
# from models import Book

db.init_app(app)
with app.app_context():
    db.create_all()

# from IPython import embed
# embed()
   
@app.route('/')
def root():
    return redirect(url_for('index'))

# INDEX
@app.route('/authors')
def index():
    return render_template('index.html', authors = Author.query.all())

# NEW
@app.route('/authors/new')
def new():
    return render_template('new.html')

# SHOW
@app.route('/authors/<int:id>')
def show(id):
    return render_template('show.html', author = Author.query.get_or_404(id))

# EDIT
@app.route('/authors/<int:id>/edit')
def edit(id):
    return render_template('edit.html', author = Author.query.get_or_404(id))

# CREATE
@app.route('/authors', methods=["POST"])
def create():
    # create python obj
    db.session.add(Book(request.form['title'],request.form['author']))
    db.session.commit()
    return redirect(url_for('index'))

# UPDATE
@app.route('/authors/<int:id>', methods=["PATCH"])
def update(id):
    found_book = Book.query.get_or_404(id)
    found_book.title = request.form['title']
    found_book.author = request.form['author']
    db.session.add(found_book)
    db.session.commit()
    return redirect(url_for('index'))

# DELETE
@app.route('/authors/<int:id>', methods=["DELETE"])
def destroy(id):
    found_book = Book.query.get_or_404(id)
    db.session.delete(found_book)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, port=3000)