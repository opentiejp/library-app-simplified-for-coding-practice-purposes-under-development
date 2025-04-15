from datetime import datetime

from library_app import db, login_manager
from flask_login import UserMixin
from pytz import timezone
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    student = db.Column(db.Boolean)
    administrator = db.Column(db.Boolean)
    librarian = db.Column(db.Boolean)
    school = db.relationship('School', backref='user', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')

    def __init__(self, email, username, password, student, administrator, librarian):
        self.email = email
        self.username = username
        self.password_hash = password
        self.student = student
        self.administrator = administrator
        self.librarian = librarian

    def __repr__(self):
        return f'UserName: {self.username}'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_student(self):
        return self.student

    def is_administrator(self):
        return self.administrator

    def is_librarian(self):
        return self.librarian

    def count_reservations(self, userid):
        return Reservation.query.filter_by(user_id=userid).count()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    author = db.Column(db.String(64), index=True)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f'Title: {self.title}, Author: {self.author}'

class Notice(db.Model):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True)
    #todo: 続きを書く


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f'ReservationID: {self.id}, User: {self.user} \n'
