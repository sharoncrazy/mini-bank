from . import core_bp
from flask import render_template, request, redirect, url_for, flash, session
from app.models import users
from app import db

@core_bp.route("/dashboard")
def dashboard():
    if 'id' not in session:
        return redirect(url_for('auth.login'))
    user = users.query.get(session['id'])
    return render_template("dashboard.html", user=user)

@core_bp.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'id' not in session:
        return redirect(url_for('auth.login'))

    user = users.query.get(session['id'])

    if request.method == 'POST':
        try:
            money = float(request.form['amount'])
            receiver_name = request.form['recipient']
            receiver = users.query.filter_by(username=receiver_name).first()

            if money <= 0:
                flash("Amount must be positive")
            elif user.balance < money:
                flash("Not enough money")
            elif not receiver:
                flash("User not found")
            elif receiver.id == user.id:
                flash("Cannot send money to yourself")
            else:
                user.balance -= money
                receiver.balance += money
                db.session.commit()
                flash(f"₹{money:.2f} sent to {receiver_name}!")
                return redirect(url_for('core.dashboard'))
        except:
            flash("Invalid amount")

    return render_template("transfer.html", user=user)