from wtforms.widgets.core import CheckboxInput

from ..models import Book
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class BookRegistrationForm(FlaskForm):
    title = StringField('書名', validators=[DataRequired(), Length(1, 64)])
    author = StringField('著者名', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('登録')


class UpdateBookForm(FlaskForm):
    title = StringField('書名', validators=[DataRequired(), Length(1, 64)])
    author = StringField('著者名', validators=[DataRequired(), Length(1, 64)])

    def __init__(self, book_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = book_id

class BookSearchForm(FlaskForm):
    search_text = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('検索')
