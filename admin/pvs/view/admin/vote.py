#This file defines all of the administrator vote pages

#Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

#PVS import
from pvs import app,db
from pvs import util
from pvs.conf import ITEMS_PER_PAGE
from pvs.core import admin_required
from pvs.model.vote import Vote,votes
from pvs.model.user import User
from pvs.form.edit import LabelEditForm,VoteEditForm,OptionEditForm,MultiEditForm
from pvs.form.vote import VoteForm,MultiCheckboxField

#WTForms imports
from wtforms import TextField,PasswordField,RadioField,SelectField,IntegerField,FloatField,BooleanField,TextAreaField,RadioField,SelectField



#Page shown when a vote is selected
@app.route('/admin/vote/<int:id>/', methods=['GET', 'POST'])
@app.route('/admin/vote/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote(id=-1):
    if not Vote.query.get(id):
	vote=Vote("New Vote")
	vote.description="Insert Description"
	vote.form=VoteForm()
	db.session.add(vote)
        db.session.commit()
	id=vote.id
	return redirect('/admin/vote/'+str(id)+"/edit")
    #Gets news story corresponding to the url
    vote=Vote.query.order_by(Vote.id).get(id)
    form=vote.form.get()
    return render_template('view/vote/admin/vote.html', vote=dict(id=vote.id,title=vote.title,description=util.sanitize(vote.description)),form=form)

#List of all votes with edit and add buttons
@app.route('/admin/votes/<int:page>/', methods=['GET', 'POST'])
@app.route('/admin/votes/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes(page=1):
    """
    Return the html string for the index page with pages for news
    @type page: number
    @param page: The current page number being viewed
    
    """
    votestable = Vote.query.order_by(Vote.time.desc()).paginate(page,ITEMS_PER_PAGE,False)
    voteslist = [dict(title=vote.title, description=util.preview(vote.description), id=vote.id,is_locked=vote.is_locked()) for vote in votestable.items]
    return render_template('view/vote/admin/votes.html', votes=voteslist,pages=votestable.pages, current_page=page)

#Adds a new checkbox
@app.route('/admin/vote/<int:id>/new/checkbox/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote_add_checkbox(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(MultiCheckboxField('Label',choices=[]))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))

#Adds a new radiofield
@app.route('/admin/vote/<int:id>/new/radiofield/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote_add_radiofield(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(RadioField('Label',choices=[]))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))
#Adds a new selectfield
@app.route('/admin/vote/<int:id>/new/selectfield/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote_add_selectfield(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(SelectField('Label',choices=[]))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))
#Adds a new integerfield
@app.route('/admin/vote/<int:id>/new/integerfield/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes_vote_add_integerfield(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(IntegerField('Label'))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))
#Adds a new floatfield
@app.route('/admin/vote/<int:id>/new/floatfield/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes_vote_add_floatfield(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(FloatField('Label'))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))
#Adds a new textbox
@app.route('/admin/vote/<int:id>/new/textarea/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes_vote_add_textarea(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(TextAreaField('Label'))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))
#Adds a new textfield
@app.route('/admin/vote/<int:id>/new/textbox/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes_vote_add_textbox(id=0):
    vote=Vote.query.get(id)
    temp=vote.form.fields
    temp.append(TextField('Label'))
    vote.form=VoteForm()
    vote.form.fields=temp
    db.session.commit()
    return redirect('/admin/vote/'+str(id)+'/edit/'+str(len(vote.form.fields)-1))

@app.route('/admin/vote/<int:id>/edit/', methods=['GET', 'POST'])
@app.route('/admin/vote/<int:id>/edit/<int:index>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_votes_vote_edit(id=1,index=-1):
    vote=Vote.query.get(id)
    if vote:
        if index<0:
            form=VoteEditForm()
    	    form.users.choices=[(str(user.id), str(user.username)) for user in User.query.order_by(User.id)]
	    if form.validate_on_submit():
	        vote.title=form.title.data
	        vote.description=form.description.data
		temp=[User.query.get(int(id)) for id in form.users.data]
		if form.grade.data=='all':
			temp +=[user for user in User.query]
		elif form.grade.data!='none':	
			temp += [user for user in User.query.filter_by(grade=form.grade.data)]
	        vote.users=temp
		vote.start_time=form.start_time.data
		vote.end_time=form.end_time.data
                db.session.commit()
	        return redirect(('/admin/vote/'+str(id)))
	    else: 
	        form.title.data=vote.title
                form.description.data=vote.description
	        form.users.data=[str(user.id) for user in vote.users]
		form.start_time.data=vote.start_time.strftime('%Y-%m-%d %H:%M:%S')
		form.end_time.data=vote.end_time.strftime('%Y-%m-%d %H:%M:%S')
	        return render_template('edit/admin/vote.html', model=vote,form=form)
        elif index<=len(vote.form.fields):
	    temp=vote.form.fields
    	    field=getattr(vote.form.get(),"id_"+str(index))
	    if isinstance(field,MultiCheckboxField):
	        form=MultiEditForm()
                if form.validate_on_submit():
	            temp[index]=type(field)(form.title.data,choices=[(str(x).strip(),str(x).strip()) for x in form.choices.data.split('\n') if str(x).strip()!=''],max_choices=int(form.max_choices.data))
	            vote.form=VoteForm()
	            vote.form.fields=temp
	            db.session.commit()
	            return redirect('/admin/vote/'+str(id))
		else:
	            form.title.data=str(field.label.text)
		    form.choices.data=str('\n'.join([c[0] for c in field.choices]))
		    form.max_choices.data=field.max_choices
	            return render_template('edit/admin/vote.html', model=vote,form=form)
	    elif isinstance(field,SelectField) or isinstance(field,RadioField):
	        form=OptionEditForm()
                if form.validate_on_submit():
	            temp[index]=type(field)(form.title.data,choices=[(str(x).strip(),str(x).strip()) for x in form.choices.data.split('\n') if str(x).strip()!=''])
	            vote.form=VoteForm()
	            vote.form.fields=temp
	            db.session.commit()
	            return redirect('/admin/vote/'+str(id))
		else:
	            form.title.data=str(field.label.text)
		    form.choices.data=str('\n'.join([c[0] for c in field.choices]))
	            return render_template('edit/admin/vote.html', model=vote,form=form)
	    else:
	        form=LabelEditForm()
	        if form.validate_on_submit():
	            temp[index]=type(field)(form.title.data)
	            vote.form=VoteForm()
	            vote.form.fields=temp
	            db.session.commit()
	            return redirect('/admin/vote/'+str(id))
	        else:
	            form.title.data=str(field.label.text)
	            return render_template('edit/admin/vote.html', model=vote,form=form)
	abort(404);

@app.route('/admin/vote/<int:id>/delete/', methods=['GET', 'POST'])
@app.route('/admin/vote/<int:id>/delete/<int:index>/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote_delete(id=1,index=-1):
    vote=Vote.query.get(id)
    if vote:
        if index<0:
            db.session.delete(vote)
            db.session.commit()
	    return redirect('/admin/votes')
        else: 
	    temp=vote.form.fields
	    vote.form=VoteForm()
	    vote.form.fields=util.list_remove(temp,index)
	    db.session.commit()
	    return redirect('/admin/vote/'+str(id))
    return redirect('/admin/votes')

@app.route('/admin/vote/<int:id>/results/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_vote_results(id=0):
    vote=Vote.query.get(id)
    if vote:
	#Gets news story corresponding to the url
    	return render_template('view/vote/admin/results.html', vote=vote)
