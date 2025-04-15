from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user

from library_app import db
from library_app.books.forms import BookRegistrationForm, UpdateBookForm
from library_app.models import Book

books = Blueprint('books', __name__)


@books.route('/book_register', methods=['GET', 'POST'])
@login_required
def book_register():
    form = BookRegistrationForm()
    if not current_user.is_librarian():
        abort(403)
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data)
        db.session.add(book)
        db.session.commit()
        flash('図書が登録されました')
        return redirect(url_for('books.book_maintenance'))
    return render_template('books/book_register.html', form=form)


@books.route('/book_maintenance')
@login_required
def book_maintenance():
    page = request.args.get('page', 1, type=int)
    books_ = Book.query.order_by(Book.id).paginate(page=page, per_page=20)
    return render_template('books/book_maintenance.html', books=books_)


@books.route('/<int:book_id>/book_details', methods=['GET', 'POST'])
@login_required
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    if not current_user.is_librarian():
        abort(403)
    form = UpdateBookForm(book_id)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.title.data
        db.session.commit()
        flash('図書詳細が更新されました')
        return redirect(url_for('books.book_maintenance'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
    return render_template('books/book_details.html', form=form)


@books.route('/<int:book_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not current_user.is_librarian():
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash('図書が削除されました')
    return redirect(url_for('books.book_maintenance'))
