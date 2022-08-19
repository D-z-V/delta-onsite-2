from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Email, EqualTo


class DeleteForm(FlaskForm):
    job_id = StringField('Job ID', validators=[InputRequired()])
    delete = SubmitField('Delete')

class ApplicationForm(FlaskForm):
    job_id = StringField('Job ID', validators=[InputRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Fullname', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    full_name = StringField('Fullname', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class JobForm(FlaskForm):
    company_name = StringField('Group Name', validators=[InputRequired()])
    position = StringField('Position', validators=[InputRequired()])
    j_d = StringField('Job Description', validators=[InputRequired()])
    expected_salary = StringField('Expected Salary', validators=[InputRequired()])
    last_date = StringField('Last Date', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    submit = SubmitField('Create Job')

