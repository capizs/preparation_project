from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    TextAreaField,
    SubmitField,
    EmailField,
    BooleanField,
)


class RegisterForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    submit = SubmitField("Войти")


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
