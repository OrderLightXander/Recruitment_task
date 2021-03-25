from flask import render_template,url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.models import User, Books, Author, Category
from flaskapp.forms import RegistrationForm, LogingForm, SearchForm
from flaskapp.utilities import find_books
from flaskapp import app, db, bcrypt


@app.route('/')
def home():
    return render_template('home.html')

#Login/Register section

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LogingForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login unseccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

# End of Login/Register section

#Books Section

@app.route('/books', methods=['GET'])
def books():
    books = Books.query.all()
    return render_template('books.html', books=books, title='All Books')

@app.route('/books_sorted_desc', methods=['GET'])
def books_sorted_desc():
    books = Books.query.order_by(Books.published_date.desc()).all()
    return render_template('books.html', books=books, title='All Books')

@app.route('/books_sorted_asc', methods=['GET'])
def books_sorted_asc():
    books = Books.query.order_by(Books.published_date.asc()).all()
    return render_template('books.html', books=books, title='All Books')

@app.route('/books/<string:value_name>/<string:filtered_value>', methods=['GET'])
def filtered_books(filtered_value, value_name):
    if value_name == 'published_date':
        books = Books.query.filter_by(published_date=filtered_value)
    if value_name == 'categories':
        books = Books.query.join(Books.categories, aliased=True).filter_by(category_name=filtered_value)
    if value_name == 'authors':
        books = Books.query.join(Books.authors, aliased=True).filter_by(author_name=filtered_value)
    return render_template('filtered_books.html', books=books, title='All Books', sort='+')

@app.route('/books<int:bookid>', methods=['GET'])
def book(bookid):
	book = Books.query.get_or_404(bookid)
	return render_template('book.html', title=book.title, book=book)

#End of Book Section

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        books_info = find_books(form.search.data)
        for value in books_info:
            # Check Books by Title
            if not Books.query.filter_by(title=value.get('title')).first():
                books = Books(title=value.get('title'), published_date=value.get('published_date')[:4], average_rating=value.get('average_rating'),
                        ratings_count=value.get('ratings_count'), thumblnail=value.get('thumbnail'))
                db.session.add(books)
            # Check Authors for Existance
            try:
                for author_value in value.get('authors'):
                    if not Author.query.filter_by(author_name=author_value).first():
                        authors = Author(author_name=author_value)
                        authors.authors.append(books)
                        db.session.add(authors)
                    else:
                        authors = Author.query.filter_by(author_name=author_value).first()
                        authors.authors.append(books)
                        db.session.add(authors)
            except TypeError:
                pass
            # Check Categories for Existance
            try:
                for category_value in value.get('categories'):
                    if not Category.query.filter_by(category_name=category_value).first():
                        category = Category(category_name=category_value)
                        category.categories.append(books)
                        db.session.add(category)
                    else:
                        category = Category.query.filter_by(category_name=category_value).first()
                        category.categories.append(books)
                        db.session.add(category)
            except TypeError:
                pass
            # Commit Books
        db.session.commit()
        flash(books_info[0].get('title'), 'success')
        return redirect(url_for('search'))
    return render_template('search.html', form=form)

#End of Login/Register section


#Database debuging tool section

@app.route('/sql_admin', methods=['GET', 'POST'])
@login_required
def sql_admin():
	books = Books.query.all()
	authors = Author.query.all()
	categories = Category.query.all()
	return render_template('sql_admin.html', title='Database', books=books, authors=authors, categories=categories)