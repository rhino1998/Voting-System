#This file defines the homepage

#Flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.login import current_user , login_required

#PVS import
from pvs import app

#Defines the homepage
@app.route('/')
def home():
	return render_template('view/home/home.html')
