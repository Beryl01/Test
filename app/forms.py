from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Property


from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, IntegerField,SelectField,FileField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileAllowed,FileRequired



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class PropertyForm(FlaskForm):

    content = TextAreaField('Describe your property', validators=[Required()])
    contact = StringField('Contact', validators=[DataRequired()])
    location = SelectField('Location', choices=[('nairobi', 'nairobi'), ('mombasa', 'mombasa'), ('kisumu', 'kisumu')],
                           validators=[Required()])

    rent = IntegerField('Rent amount', validators=[Required()])


    submit = SubmitField('Post')


