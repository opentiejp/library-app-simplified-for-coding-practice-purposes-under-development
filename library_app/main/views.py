from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import desc

from library_app import db
from library_app.books.forms import BookSearchForm
from library_app.main.image_handler import add_featured_image
from library_app.models import Book, Notice

from unicodedata import normalize

main = Blueprint('main', __name__)

@main.route('/')
def index():
    form = BookSearchForm()

    page = request.args.get('page', 1, type=int)
    notice_posts = Notice.query.order_by(desc(Notice.id)).paginate(page=page, per_page=10)

    return render_template('index.html', notice_posts=notice_posts, form=form)

@main.route('/search', methods=['GET', 'POST'])
def book_search():
    form = BookSearchForm()
    search_text = ""
    if form.validate_on_submit():
        search_text = form.search_text.data
    elif request.method == 'GET':
        form.search_text.data = ""
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter((Book.text.contains(search_text)) | (Book.title.contains(search_text)) | (Book.author.contains(search_text))).order_by(desc(Book.id)).paginate(page=page, per_page=20)

    return render_template('index.html', books=books, form=form, search_text=search_text)

@main.route('/info')
def info():
    return render_template('info.html')
