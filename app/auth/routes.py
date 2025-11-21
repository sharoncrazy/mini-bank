from . import auth_bp
from flask import render_template, request, redirect, url_for, flash, session
from app.models import users
from app import db

@auth_bp.route('/')
def home():
    return render_template("signup.html")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = users.authenticate(username, password)

        if user and user.check_password(password):
            session['id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('core.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password != confirm_password:
            flash("Password does not match")
            return redirect(url_for('auth.home'))
        
        if users.query.filter_by(username=username).first():
            flash('Username taken!')
            return redirect(url_for('auth.home'))

        if users.get_by_username(username):  
            flash('Username already taken!')
            return redirect(url_for('auth.home'))
        
        users.create_user(username, password)
        db.session.commit()

        flash('Account created! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('auth.home'))