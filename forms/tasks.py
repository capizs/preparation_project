import sqlalchemy.orm as orm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    answer = StringField("Ответ", validators=[DataRequired()])
    submit = SubmitField("Ответить")
