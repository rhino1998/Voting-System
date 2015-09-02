#This file defines the documentation system

#Misc imports
import os


#Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

#PVS import
from pvs import app,db
from pvs import util
from pvs.core import admin_required
from pvs.conf import ITEMS_PER_PAGE


#The documentation page, it shows documentation
@app.route('/admin/docs/', methods=['GET', 'POST'])
@app.route('/admin/docs/<path:path>/', methods=['GET', 'POST'])
@app.route('/admin/docs/<path:path>/<file:filename>', methods=['GET', 'POST'])
@login_required
@admin_required
def docs(path='',filename='readme.md'):
    current_file=os.path.join(path,filename)
    if os.path.isdir(current_file):
	current_file=os.path.join(current_file,'readme.md')
    if current_file.endswith(".md"):
	header=''
    else:	
	header=current_file
    if not os.path.exists(current_file):
	return abort(404)
    return render_template('view/docs/docs.html',content=util.doc(current_file),header=header)

      



