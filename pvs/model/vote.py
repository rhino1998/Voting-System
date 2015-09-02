#This file defines the models for the voting tables

#Misc imports
import time
import datetime
#PVS imports
from pvs import app,db


#Relationship table for users and votes
votes = db.Table('votes',
	db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
	db.Column('vote_id',db.Integer,db.ForeignKey('vote.id')),sqlite_autoincrement=True)

#Model for votes
class Vote(db.Model):
    """Table model for 
    """
    #SQL table defines
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.Text, default="Description here")
    results = db.Column(db.PickleType(comparator=lambda *a: False))
    form=db.Column(db.PickleType())
    time = db.Column(db.DateTime)
    #Checks times
    def is_locked(self):
	return self.results!=[] or self.is_active()
    def is_active(self):
	return self.start_time < datetime.datetime.utcnow() < self.end_time
    #Row initialization
    def __init__(self, title):
	self.title = title[0].upper()+title[1:]
	self.time=datetime.datetime.utcnow()
	self.start_time=(datetime.datetime.utcnow()-datetime.timedelta(seconds=1))
	self.end_time=(datetime.datetime.utcnow())
	self.results=[]
    #Basically toString()
    def __repr__(self):
        return '<Vote %r>' % self.title


