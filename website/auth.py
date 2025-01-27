# app/auth.py
from flask import render_template, request, redirect, url_for, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from .models import User  # Mengimpor model User

auth = Blueprint('auth',__name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Hashed password: {hashed_password}")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username sudah digunakan')
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html',user = current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('views.home'))  # Redirect to a home page after login
        else:
            flash('Login failed. Check your username and/or password.', 'danger')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))