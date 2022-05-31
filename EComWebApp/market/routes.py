from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForms, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if purchase_form.validate_on_submit():
        print(purchase_form['purchased_item'])
    items = Item.query.all()
    return render_template("market.html", items=items, purchase_form=purchase_form)

@app.route('/register', methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
         user_to_create = User(username=form.username.data, email_address = form.email_address.data, password= form.password1.data)
         db.session.add(user_to_create)
         db.session.commit()
         login_user(user_to_create)
         flash(f'Account created successfully. You are logged in as {user_to_create.username}', category='success')
         return redirect(url_for('market_page'))
    if form.errors != {}: #if there re no errors from validation
        for err_msg in form.errors.values():
            flash(f"There was error creating user: {err_msg}", category='danger')
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login_page():
    form = LoginForms()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as :{attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('User name and password dont match. Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for("home_page"))
