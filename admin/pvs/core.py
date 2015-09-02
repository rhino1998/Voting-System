"""This file contains functions that
are integral to the function of the package,
but do not fit in a subfolder
"""

#Misc imports
import os
from functools import wraps

#PVS imports
import pvs.util
from pvs import app, login_manager
from pvs.model.user import User
from pvs.conf import APPNAME
#Flask imports
from flask import request, send_from_directory, g, redirect, url_for, render_template, flash
from flask.ext.login import current_user

@login_manager.user_loader
def load_user(id_):
    """A utility function that returns user with id (id) to the login manager
    """
    return User.query.get(int(id_))

@app.before_request
def before_request():
    """Sets the global (g) context variable user to current_user
    """
    g.user = current_user
    g.appname = APPNAME

@app.route('/favicon.ico')
def favicon():
    """Defines Favicon path
    """
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(404)
def page_not_found(e):
    """Defines a custom 404 page
    """
    return render_template('view/error/404.html', APPNAME=APPNAME, e=e)

def admin_required(f):
    """Requires admininstrator access to certain views
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Requires the user to be an administrator
        """
        if not g.user is None and not g.user.is_admin():
            flash('You must be an administrator to access this page')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
