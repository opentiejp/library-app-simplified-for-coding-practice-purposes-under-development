from email_validator.rfc_constants import EMAIL_MAX_LENGTH
from wtforms.widgets.core import CheckboxInput

from ..models import User
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class UserRegistrationForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください'), Length(max=EMAIL_MAX_LENGTH)])
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('<PASSWORD>', validators=[DataRequired(), EqualTo('pass_confirm', message='パスワードが一致していません')])
    pass_confirm = PasswordField('パスワード(確認)', validators=[DataRequired()])
    is_student = BooleanField('生徒', default=True, widget=CheckboxInput())
    is_administrator = BooleanField('管理者', default=False, widget=CheckboxInput())
    is_librarian = BooleanField('司書', default=False, widget=CheckboxInput())
    submit = SubmitField('登録')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名はすでに使われています。')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスはすでに登録されています。')


class UpdateUserForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[EqualTo('pass_confirm', message='パスワードが一致していません')])
    pass_confirm = PasswordField('パスワード(確認)')
    submit = SubmitField('更新')

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = user_id

    def validate_email(self, field):
        if User.query.filter(User.id != self.id).filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスはすでに登録されています。')

    def validate_username(self, field):
        if User.query.filter(User.id != self.id).filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名はすでに使われています。')
