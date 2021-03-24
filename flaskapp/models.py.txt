from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)


authors = db.Table('author_relations',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'))
)

categories = db.Table('category_relations',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    authors = db.relationship('Author', secondary=authors, backref=db.backref('authors', lazy='dynamic'))
    published_date = db.Column(db.String(5), nullable=True)
    categories = db.relationship('Category', secondary=categories, backref=db.backref('categories', lazy='dynamic'))
    average_rating = db.Column(db.String(10), nullable=True)
    ratings_count = db.Column(db.String(10), nullable=True)
    thumblnail = db.Column(db.String(100), nullable=True)


class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(30))



class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(30))