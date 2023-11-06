from flask import Blueprint, render_template, request, redirect, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from app import db
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login_page():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return render_template('login.html')

    login_user(user)
    return redirect(url_for('dashboard.user_dashboard_page'))


@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register')
def register_page():
    errors_bag = []
    cached_data = []
    return render_template('register.html', errors_bag=errors_bag, cached_data=cached_data)


@auth.route('/register', methods=['POST'])
def register():

    errors_bag = []
    cached_data = {}
    cached_data['name'] = name = request.form.get('name')
    cached_data['email'] = email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if len(password) < 8:
        errors_bag.append("Password must be over 7 characters")
    if confirm_password != password:
        errors_bag.append("Passwords not match")

    user = User.query.filter_by(email=email).first()

    if user:
        errors_bag.append("User "+email+" already exists!")

    if len(errors_bag) > 0:
        return render_template('register.html', errors_bag=errors_bag, cached_data=cached_data)

    new_user = User(name=name, email=email, password=generate_password_hash(password, rounds=10))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login_page'))
