from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional

class Register(FlaskForm):
    fName = StringField('First Name',validators=[DataRequired(),Length(min=3,max=20)])
    lName = StringField('Last Name',validators=[DataRequired(),Length(min=3,max=20)])
    username = StringField('UserName',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

class Login(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('login')
    remember = BooleanField('Remember')

class Edit_Profile(FlaskForm):
    username=StringField(' Another UserName',validators=[Optional(),Length(min=2,max=20)])
    email = StringField(' Another Email',validators=[Optional(),Email()])
    submit = SubmitField('Change')

class Reset_Request_Form(FlaskForm):
    email = StringField(' Enter your email ', validators=[Optional(), Email()])
    submit = SubmitField('Send')

class Reset_Password(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('change')
