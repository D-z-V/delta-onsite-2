from email.mime import application
from forms import LoginForm, RegisterForm, JobForm, ApplicationForm, DeleteForm
from flask import Flask, render_template, abort, request, session
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import random
import string
import datetime
import os

app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    j_d = db.Column(db.String(20), nullable=False)
    expected_salary = db.Column(db.String(20), nullable=False)
    last_date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)
    admin = db.relationship('Admin', backref=db.backref('jobs', lazy=True))

class Applications(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['user_id'] = user.user_id
                session['full_name'] = user.full_name
                return redirect(url_for('user_home'))
            else:
                return render_template('user_login.html', form=form, error='Invalid password')
        else:
            return render_template('user_login.html', form=form, error='Invalid email')
    return render_template('user_login.html', form=form)

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.query.count() + 1
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_id=user_id, full_name=form.full_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('user_register.html', form=form)


@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if 'user_id' in session:
        form = ApplicationForm()
        jobs = Job.query.all()
        if form.validate_on_submit():
            application_id = Applications.query.count() + 1
            application = Applications(application_id=application_id, user_id=session['user_id'], job_id=form.job_id.data)
            db.session.add(application)
            db.session.commit()
            return redirect(url_for('user_home'))
        return render_template('user_home.html', form=form, jobs=jobs)
    else:
        return redirect(url_for('user_login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin:
            if bcrypt.check_password_hash(admin.password, form.password.data):
                session['admin_id'] = admin.admin_id
                session['full_name'] = admin.full_name
                return redirect(url_for('admin_home'))
            else:
                return render_template('admin_login.html', form=form, error='Invalid password')
        else:
            return render_template('admin_login.html', form=form, error='Invalid email')
    return render_template('admin_login.html', form=form)

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    form = RegisterForm()
    if form.validate_on_submit():
        admin_id = Admin.query.count() + 1
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(admin_id=admin_id, full_name=form.full_name.data, email=form.email.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('admin_login'))
    return render_template('admin_register.html', form=form)

@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    form = JobForm()
    del_form = DeleteForm()
    
    if 'admin_id' in session:
        if form.validate_on_submit():
            job_id = Job.query.count() + 1
            job = Job(job_id=job_id, company_name=form.company_name.data, position=form.position.data, j_d=form.j_d.data, expected_salary=form.expected_salary.data, last_date=form.last_date.data, location=form.location.data, admin_id=session['admin_id'])
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('admin_home'))

        if del_form.validate_on_submit():
            job = Job.query.filter_by(job_id=del_form.job_id.data).first()
            db.session.delete(job)
            db.session.commit()
            return redirect(url_for('admin_home'))

        jobs = Job.query.filter_by(admin_id=session['admin_id']).all()

        applications = []

        for job in jobs:
            applications.append(Applications.query.filter_by(job_id=job.job_id).all())


        return render_template('admin_home.html', form=form, jobs=jobs, del_form=del_form, applications=applications)
    else:
        return redirect(url_for('admin_login'))




@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)