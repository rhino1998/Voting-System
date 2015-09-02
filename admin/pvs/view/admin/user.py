#This file contains the administrator user views

#Flask Import
from flask import Flask,current_app, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required, login_user, LoginManager , logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form

#PVS imports
from pvs import app,db
from pvs.core import admin_required
from pvs.conf import ITEMS_PER_PAGE
from pvs.model.user import User, UserKey
from pvs.model.vote import Vote,votes
from pvs.form.edit import UserEditForm
from pvs.form.user import KeyCreateForm



#Lists Users
@app.route('/admin/users/', methods=['GET', 'POST'])
@app.route('/admin/users/<int:page>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users(page=1):
    userstable = User.query.order_by(User.username.desc()).paginate(page,ITEMS_PER_PAGE,False)
    userslist = [dict(username=user.username, grade=user.grade, admin=user.admin , id=user.id) for user in userstable.items]

    return render_template('view/user/admin/users.html', users=userslist,pages=userstable.pages, current_page=page)
#Shows information on one user
@app.route('/admin/user/', methods=['GET', 'POST'])
@app.route('/admin/user/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user(id=0):
    if not User.query.get(id):
	user=User()
	user.username="Username"
	db.session.add(user)
        db.session.commit()
	id=user.id
	return redirect('/admin/user/'+str(id)+"/edit")
    user=User.query.get(id)
    return render_template('view/user/admin/user.html', user=user)
#Deletes a user
@app.route('/admin/user/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_delete(id=1):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin/users')

#Edit User
@app.route('/admin/user/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_edit(id=0):
    user=User.query.get(id)
    form=UserEditForm()
    print(User.query.filter_by(username=form.username.data).first(),form.username.data!=user.username)
    if form.validate_on_submit() and not (User.query.filter_by(username=form.username.data).first() is not None and form.username.data!=user.username):
	user.set_password(form.password.data)
        user.username=form.username.data
        user.grade=form.grade.data
	user.admin=form.admin.data
        db.session.commit()
        return redirect('/admin/users/')
    else: 
	if (User.query.filter_by(username=form.username.data).first() is not None and form.username.data!=user.username):
	    flash('Username was taken')
        form.username.data=user.username
        form.grade.data=user.grade
	form.admin.data=user.admin
        return render_template('edit/admin/user.html', model=user,form=form)
#Shows the key list
@app.route('/admin/keys/', methods=['GET', 'POST'])
@app.route('/admin/keys/<int:page>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_keys(page=1):
	keystable=UserKey.query.paginate(page,ITEMS_PER_PAGE,True)
	keylist = [dict(key=key.key, id=key.id) for key in keystable.items]
	return render_template('view/user/admin/keys.html', keys=keylist,pages=keystable.pages, current_page=page)
#Easily prinatble keylist
@app.route('/admin/print_keys/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_print_keys():
	keystable=UserKey.query
	keylist = [key.key for key in keystable]
	return render_template('view/user/admin/print_keys.html', keys=keylist)
#Creates x number of keys
@app.route('/admin/create_keys/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_create_keys():
	form=KeyCreateForm()
	if form.validate_on_submit():
		for i in range(form.keys.data):
			db.session.add(UserKey())
		db.session.commit()
		return redirect('/admin/keys')
	else:
		return render_template('view/user/admin/create_keys.html',form=form)
#Deletes all keys
@app.route('/admin/delete_keys/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_delete_keys():
    UserKey.query.delete()
    db.session.commit()
    return redirect('/admin/keys')
#Deletes an individual key
@app.route('/admin/key/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_key_delete(id=1):
    key=UserKey.query.get(id)
    db.session.delete(key)
    db.session.commit()
    return redirect('/admin/keys')

