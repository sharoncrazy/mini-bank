from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from models import users



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bankuser:bankpass@localhost:5432/mini bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home() :
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template ("login.html")


@app.route('/signup',methods=["POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']

        if password != confirm_password :
            flash("Password does not match")
            return redirect(url_for("signup.html"))
        
        if users.query.filter_by(username=username).first():
            flash('Username taken!')
            return redirect(url_for('signup'))

        user = users(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signed up! Log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

        
    






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)