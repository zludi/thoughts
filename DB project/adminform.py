from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
 
 
class AdminForm(FlaskForm):
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')