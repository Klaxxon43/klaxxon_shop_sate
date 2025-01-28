from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, BooleanField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileAllowed
# from .main import Users

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Почта', validators=[DataRequired(), Length(min=2, max=50)])
    # status = SelectField('Статус', choices=['Родитель', 'Воспитатель'], render_kw={'class':'form-control'}, default='Родитель', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    image_url = FileField('Изображение', validators=[FileAllowed((['jpg', 'png', 'jpeg']))])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class ItemForm(FlaskForm):
    game = SelectField('Игра', choices=['Brawl Stars', 'Clash of Clans', 'Clash Royale'], render_kw={'class':'form-control'}, default='Brawl Stars', validators=[DataRequired()])
    category = SelectField('Категория', choices=['Гемы', 'Акции', 'Донат', 'Буст', 'Прочее'], render_kw={'class':'form-control'}, default='SUPERSELL ID', validators=[DataRequired()])
    name = StringField('Название товара', validators=[DataRequired(), Length(min=2, max=50)])
    price = IntegerField('Цена', validators=[DataRequired()]) 
    image_url = FileField('Изображение', validators=[FileAllowed((['jpg', 'png', 'jpeg']))])
    description = StringField('Описание', validators=[DataRequired()])
    delivery = SelectField('Способ получения', choices=['SUPERSELL ID', 'PLAYER TAG'], render_kw={'class':'form-control'}, default='SUPERSELL ID', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')


class IncreaseBasketForm(FlaskForm):
    action = HiddenField('action', default='increase') # Добавим HiddenField для action, хотя он и так задан в value
    submit = SubmitField('+', render_kw={'class': 'btn btn-primary'}) # Кнопка "+"

class DecreaseBasketForm(FlaskForm):
    action = HiddenField('action', default='decrease') # Добавим HiddenField для action
    submit = SubmitField('-', render_kw={'class': 'btn btn-primary', 'style': 'margin-left: 50%; margin-top: -60px;'}) # Кнопка "-"

class RemoveFromBasketForm(FlaskForm):
    submit = SubmitField('Удалить', render_kw={'class': 'btn btn-danger', 'style': 'margin-top: -30px;'}) # Кнопка "Удалить"
class StudentForm(FlaskForm):
    student = SelectField('student', choices=[], render_kw={'class':'form-control'})

class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[], render_kw={'class':'form-control'})
