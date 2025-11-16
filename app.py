from flask import Flask,render_template,request,flash,redirect,url_for,session
from db import db
from models import users




#CONFIG
app = Flask(__name__)
app.secret_key = 'mini-bank-secret-key-2025-do-not-share'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bankuser:bankpass@localhost:5432/mini-bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home() :
    return render_template("signup.html")

#Already have an account
@app.route("/exist_login")
def exist_login():
    return render_template ("login.html")

#signup
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

#login
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


#Dashboard (Home page)
@app.route("/dashboard")
def dashboard():
    user = users.query.get(session['id'])
    
    return render_template("dashboard.html",user=user)


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    user = users.query.get(session['id'])
    if request.method == 'POST':
        

        money = float(request.form['amount'])
        receiver_name = request.form['recipient']

        receiver = users.query.filter_by(username=receiver_name).first()

        if user.balance < money :
            flash("Not enough money")
        elif not receiver :
            flash("User not found")
        elif money <= 0 :
            flash("Amount must be positive")
        else :
            user.balance -= money 
            receiver.balance += money
            db.session.commit()
            flash(f"₹{money:.2f} sent to {receiver_name}!")
            return redirect(url_for('dashboard'))
        
        
        
        




    return render_template("transfer.html",user=user)




            




        
    






if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)