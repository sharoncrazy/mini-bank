from flask import Flask,render_template,request,flash,redirect,url_for,session
from db import db
from models import users
import os



#CONFIG
app = Flask(__name__)
app.secret_key = 'mini-bank-secret-key-2025-do-not-share'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bankuser:bankpass@localhost:5432/mini-bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home() :
    return render_template("signup.html")

@app.route("/exist_login")
def exist_login():
    return render_template ("login.html")


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password != confirm_password :
            flash("Password does not match")
            return redirect(url_for("home"))
        
        if users.query.filter_by(username=username).first():
            flash('Username taken!')
            return redirect(url_for('home'))

        user = users(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signed up! Log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST" :
        username = request.form['username']
        password = request.form['password']

        user = users.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['id'] = user.id
            session['username'] = user.username

            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')
            




        
    






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)