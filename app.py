from flask import Flask, render_template, request, redirect, url_for
from shared import db
from models import Author
from models import Book
from models import Tag
# Flask - class used to initialize an app
# render_template - render a template
# request - getting form data via POST request
# redirect - respond with location header
# url_for - shorthand for using function name instead of name of route

from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/python_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# trees the route with a trailing / without the /. ex. author/3/ will not give an error because of FALSE
app.url_map.strict_slashes = False

# Modus - allows us to do method override via headers or query string
# with ?_method
# from models import Book

db.init_app(app)
with app.app_context():
    db.create_all()

def get_tags_from_form():
    tag_ids_from_form = [int(tag) for tag in request.form.getlist('tags')]
    return [tag for tag in Tag.query.all() if tag.id in tag_ids_from_form]

   
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

# author routes

@app.route('/authors', methods=["GET"])
def index_author():
    return render_template('authors/index.html', authors=Author.query.order_by(Author.id).all())

@app.route('/authors', methods=["POST"])
def create_author():
    db.session.add(Author(request.form['name']))
    db.session.commit()
    return redirect(url_for('index_author')) 

@app.route('/authors/new', methods=["GET"])
def new_author():
    return render_template('authors/new.html')

@app.route('/authors/<id>/edit', methods=["GET"])
def edit_author(id):
    return render_template('authors/edit.html', author=Author.query.get_or_404(id))

@app.route('/authors/<id>', methods=["GET"])
def show_author(id):
    return render_template('authors/show.html', author=Author.query.get_or_404(id))

@app.route('/authors/<id>', methods=["PATCH"])
def update_author(id):
    author = Author.query.filter_by(id=id).first_or_404()
    author.name = request.form['name']
    db.session.add(author)
    db.session.commit()
    return redirect(url_for('index_author'))

@app.route('/authors/<id>', methods=["DELETE"])
def destroy_author(id):
    db.session.delete(Author.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('index_author'))      

# book routes

@app.route('/authors/<id>/books', methods=["GET"])
def index_book(id):
    return render_template('books/index.html', author=Author.query.get_or_404(id))

@app.route('/authors/<id>/books', methods=["POST"])
def create_book(id):
    book = Book(request.form['title'], id)
    book.tags = get_tags_from_form()
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index_book', id=id)) 

@app.route('/authors/<id>/books/new', methods=["GET"])
def new_book(id):
    return render_template('books/new.html', author=Author.query.get_or_404(id), tags=Tag.query.all())

@app.route('/authors/<id>/books/<book_id>/edit', methods=["GET"])
def edit_book(id,book_id):
    return render_template('books/edit.html', book=Book.query.get_or_404(book_id), tags=Tag.query.all())

@app.route('/authors/<id>/books/<book_id>', methods=["GET"])
def show_book(id,book_id):
    return render_template('books/show.html', book=Book.query.get_or_404(book_id), author=Author.query.get_or_404(id))

@app.route('/authors/<id>/books/<book_id>', methods=["PATCH"])
def update_book(id,book_id):
    book = Book.query.filter_by(id=book_id).first_or_404()
    book.title = request.form['title']
    book.tags = get_tags_from_form()
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index_book', id=id))

@app.route('/authors/<id>/books/<book_id>', methods=["DELETE"])
def destroy_book(id,book_id):
    db.session.delete(Book.query.get_or_404(book_id))
    db.session.commit()
    return redirect(url_for('index_book', id=id))  

#tag routes
@app.route('/tags', methods=["GET"])
def index_tag():
    return render_template('tags/index.html', tags=Tag.query.all())

@app.route('/tags/new', methods=['GET'])
def new_tag():
    return render_template('tags/new.html')

@app.route('/tags', methods=["POST"])
def create_tag():
    tag = Tag(request.form['genre'])
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('index_tag')) 

@app.route('/tags/<tag_id>', methods=['GET'])
def show_tag(tag_id):
    return render_template('tags/show.html',  tag=Tag.query.get_or_404(tag_id))   

@app.route('/tags/<tag_id>/edit', methods=['GET'])
def edit_tag(tag_id):
    return render_template('tags/edit.html', tag=Tag.query.get_or_404(tag_id))   

@app.route('/tags/<tag_id>', methods=["PATCH"])
def update_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    tag.genre = request.form['genre']
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('index_tag', id=tag_id))

@app.route('/tags/<tag_id>', methods=["DELETE"])
def destroy_tag(tag_id):
    db.session.delete(Tag.query.get_or_404(tag_id))
    db.session.commit()
    return redirect(url_for('index_tag', id=tag_id))  


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)