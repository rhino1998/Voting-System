#This file defines the non-admin user views including login,logout, registration, and account editing

#Flask Import
from flask import Flask,current_app, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required, login_user, LoginManager , logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form

#PVS imports
from pvs import app,db
from pvs.model.user import User,UserKey
from pvs.model.vote import Vote,votes
from pvs.form.user import LoginForm,RegisterForm
from pvs.form.edit import AccountEditForm



#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Compare passwords (hashed)
        if not user is None and user.check_password(form.password.data):
            # Keep the user info in the session using Flask-Login
            login_user(user)

            return redirect(request.args.get('next') or '/')
	else:
	    flash('Invalid username or password')

    return render_template('view/user/login.html', form=form)

#Logout
@app.route('/logout')
def logout():
    #Logs user out
    logout_user()
    return redirect(request.args.get('next') or '/')



#Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Validate form input
    if form.validate_on_submit():
        # Retrieve the user from the datastore
        user = User()
        user.username=form.username.data
        user.set_password(form.password.data)
        user.grade=form.grade.data
        user.admin=False
	key=UserKey.query.filter_by(key=form.key.data).first()
	db.session.add(user)
	db.session.delete(key)
	db.session.commit()
        return redirect('/login')
    return render_template('view/user/register.html', form=form)



#Edit Account
@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account_edit():
    user=User.query.get(g.user.id)
    form=AccountEditForm()
    if form.validate_on_submit() and not (User.query.filter_by(username=form.username.data).first() is not None and form.username.data!=user.username):
	user.set_password(form.password.data)
        user.username=form.username.data
        db.session.commit()
        return redirect('/')
    else: 
	if (User.query.filter_by(username=form.username.data).first() is not None and form.username.data!=user.username):
	    flash('Username was taken')
        form.username.data=user.username
        return render_template('edit/account.html',form=form)

