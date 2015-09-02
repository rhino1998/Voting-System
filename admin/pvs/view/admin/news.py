#This file defines the administrator newspages

#Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

#PVS import
from pvs import app,db
from pvs import util
from pvs.core import admin_required
from pvs.conf import ITEMS_PER_PAGE
from pvs.model.news import News
from pvs.model.user import User
from pvs.form.edit import LabelEditForm,VoteEditForm,NewsEditForm

#WTForms imports
from wtforms import TextField,PasswordField


#Shows newslist with edit and delete buttons
@app.route('/admin/news/', methods=['GET', 'POST'])
@app.route('/admin/news/<int:page>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_news(page=1):
    newstable = News.query.order_by(News.time.desc()).paginate(page,ITEMS_PER_PAGE,False)
    newslist = [dict(title=article.title, body=util.preview(article.body), id=article.id) for article in newstable.items]

    return render_template('view/news/admin/news.html', news=newslist,pages=newstable.pages, current_page=page)

#Shows individual article
@app.route('/admin/article/', methods=['GET', 'POST'])
@app.route('/admin/article/<int:id>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_article(id=0):
    if not News.query.get(id):
	article=News("New Article")
	article.body="Insert Body"
	db.session.add(article)
        db.session.commit()
	id=article.id
	return redirect('/admin/article/'+str(id)+"/edit")
    #Gets news story corresponding to the url
    article=News.query.get(id)
    print(util.sanitize(article.body))
    return render_template('view/news/article.html', article=dict(id=article.id,title=article.title,body=util.sanitize(article.body)))

#Shows article edit page
@app.route('/admin/article/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_article_edit(id=0):
    article=News.query.get(id)
    form=NewsEditForm()
    if form.validate_on_submit():
        article.title=form.title.data
        article.body=form.body.data
        db.session.commit()
        return redirect('/admin/news/')
    else: 
        form.title.data=article.title
        form.body.data=article.body
        return render_template('edit/admin/article.html', model=article,form=form)
#Deletes article
@app.route('/admin/article/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_article_delete(id=1,index=-1):
    article=News.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/admin/news')
