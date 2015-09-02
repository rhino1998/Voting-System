#This file defines all the non-admin vote views

#Misc imports
import math

#Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

#PVS import
from pvs import app,db
from pvs import util
from pvs.conf import ITEMS_PER_PAGE
from pvs.model.vote import Vote
from pvs.model.user import User
from pvs.form.edit import LabelEditForm,VoteEditForm
from pvs.form.vote import VoteForm,MultiCheckboxField

#WTForms imports
from wtforms import TextField,PasswordField


#The votes page, it shows votes
@app.route('/votes/', methods=['GET', 'POST'])
@app.route('/votes/<int:page>/', methods=['GET', 'POST'])
@login_required
def votes(page=1):
    """
    Return the html string for the index page with pages for news
    @type page: number
    @param page: The current page number being viewed
    
    """
    votes = sorted(g.user.votes,key=lambda x: x.end_time)
    votes = filter(lambda x:x.is_active(),votes)
    voteslist = [dict(title=vote.title, description=util.preview(vote.description), id=vote.id,end_time=vote.end_time) for vote in votes[max(0,page-ITEMS_PER_PAGE):min(len(votes),page+ITEMS_PER_PAGE)]]
    return render_template('view/vote/votes.html', votes=voteslist,pages=int(math.ceil(len(votes)/ITEMS_PER_PAGE)), current_page=page)

#Page shown when a vote is selected
@app.route('/vote/<int:id>/', methods=['GET', 'POST'])
@login_required
def vote(id=1):
    #Gets vote corresponding to the url
    vote=Vote.query.order_by(Vote.id).get(id)
    form=vote.form.get()
    if form.validate_on_submit():
	results=[]
	#Compiles results
	for i in range(len(vote.form.fields)):
	    field=getattr(form,"id_"+str(i))
	    if isinstance(field.data,list):
		temp=[]
		for datum in field.data:
		    temp.append([str(datum),1])
		if hasattr(field,'max_choices') and field.max_choices>0:
		    temp=temp[:min(field.max_choices,len(temp))]
	        results.append(dict(index=i,label=str(field.label.text),data=temp))
	    else:
		results.append(dict(index=i,label=str(field.label.text),data=[[str(field.data),1]]))
	vote.results=util.combine_results(vote.results,results)
	g.user.votes.remove(vote)
	db.session.commit()
	return redirect('/votes/')
    else:
    	return render_template('view/vote/vote.html', vote=dict(id=vote.id,title=vote.title,description=util.sanitize(vote.description)),form=form)


      



