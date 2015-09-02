#This file defines the non-admin newspages

#Flask Imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

#PVS imports
from pvs import app,db,util
from pvs.conf import ITEMS_PER_PAGE
from pvs.model.news import News
from pvs.form.edit import NewsEditForm

#The news list page
@login_required
@app.route('/news/', methods=['GET', 'POST'])
@app.route('/news/<int:page>/', methods=['GET', 'POST'])
def news(page=1):
    #Gets a list of all news articles
    newstable = News.query.order_by(News.time.desc()).paginate(page,ITEMS_PER_PAGE,True)
    newslist = [dict(title=article.title, body=util.preview(article.body), id=article.id, time=article.time) for article in newstable.items]
    return render_template('view/news/news.html', news=newslist,pages=newstable.pages, current_page=page)

#Individual article
@login_required
@app.route('/article/', methods=['GET', 'POST'])
@app.route('/article/<int:id>/', methods=['GET', 'POST'])
def article(id=0):
    if News.query.get(id):
	#Gets news story corresponding to the url
    	article=News.query.get(id)
    	return render_template('view/news/article.html', article=dict(id=article.id,title=article.title,body=util.sanitize(article.body)))

