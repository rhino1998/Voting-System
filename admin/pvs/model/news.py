#This file defines the article model

import datetime
from pvs import db

#Table model for news stories
class News(db.Model):
    """Table model for 
    """
    #SQL table defines
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    #Row initialization
    def __init__(self, title):
        self.title = title[0].upper()+title[1:]
    #Basically toString()
    def __repr__(self):
        return '<News %r>' % self.title
