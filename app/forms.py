from random import choices

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, length, EqualTo, ValidationError

from .models.user import User


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), length(min=4, max=100)])
    login = StringField(validators=[DataRequired(), length(min=2, max=20)])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    status = BooleanField('Статус учителя')
    avatar = FileField(validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Зарегистрировать')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError("Данное имя пользователя уже занято. Пожалуйста, выберите другое...")


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired(), length(min=2, max=10)])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField("Запомнить меня!")
    submit = SubmitField("Войти")


class StudentForm(FlaskForm):
    student = SelectField('student', choices=[], render_kw={'class':'form-control'})