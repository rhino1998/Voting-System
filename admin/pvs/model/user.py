#This file defines the models used to control the user system

import uuid
from pvs import db
from pvs import util
from pvs.model.vote import Vote,votes
from werkzeug.security import generate_password_hash,check_password_hash

#Model for userkeys
class UserKey(db.Model):
    #SQL table defines
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80),unique=True)

    #Row initalization
    def __init__(self):
        self.key=str(uuid.uuid4())[:8]
    #Basically toString()
    def __repr__(self):
        return '<UserKey %r>' % self.key

#Model for users
class User(db.Model):
    #SQL table defines
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    pw_hash = db.Column(db.String(80))
    grade = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    votes = db.relationship('Vote',secondary=votes,backref=db.backref('users',lazy='joined'),lazy='dynamic')

    #If user is authenticated
    def is_authenticated(self):
        return True

    #If user is active
    def is_active(self):
        return True

    #If user is anonymous
    def is_anonymous(self):
        return False

    #If user is admin
    def is_admin(self):
        return self.admin

    #Gets user id
    def get_id(self):
        return unicode(self.id)

    #Hashes user password
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    #Checks if user password matches hashed password
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    #Basically toString()
    def __repr__(self):
        return '<User %r>' % self.username
