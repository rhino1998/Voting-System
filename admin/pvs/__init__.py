#This file is the main project file. It initializes all necessary variables and establishes the structure of the package

#PVS imports
from pvs import conf
from pvs.util import FileConverter

#Flask imports
from flask import Flask,g
from flask.ext.assets import Environment, Bundle
from flask.ext.login import current_user , login_required, LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

# Application defines
app = Flask(conf.APPNAME)
app.config.from_object(conf)
# Database defines
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+conf.DATABASE
app.url_map.converters['file'] = FileConverter
db = SQLAlchemy(app)
# Login system defines
login_manager=LoginManager(app)
login_manager.login_view='login'
#Css manager Defines
assets=Environment(app)
css_all = Bundle(
    'less/style.less',
    filters='less, cssmin',
    output='gen/min.css',
)
assets.register('css_all', css_all)
#Web Tree imports
import pvs.core
import pvs.view.home
import pvs.view.news
import pvs.view.user
import pvs.view.vote
import pvs.view.admin.news
import pvs.view.admin.vote
import pvs.view.admin.user
import pvs.view.admin.docs


db.create_all()
