from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerRangeField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя')
    age = IntegerRangeField("Возраст пользователя")
    position = StringField("Должность")
    speciality = StringField("Профессия")
    address = StringField("Адрес участника")
    # about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')