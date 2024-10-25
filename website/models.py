from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),index=True,unique=True,nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    contact_number = db.Column(db.Integer(10), index=True, nullable=False)
    street_address = db.Column(db.String(100), index=True, nullable=False)

    comments = db.relationship('Comment',backref='user')
    events = db.relationship('Event',secondary='comments',backref=db.backref('commented_users'))

class Event(db.Model):
    __tablename__='events'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(1000), nullable=False)
    location=db.Column(db.String(200),nullable=False)
    time=db.Column(db.DateTime,nullable=False)
    contact_number = db.Column(db.Integer(10), index=True, nullable=False)
    street_address = db.Column(db.String(100), index=True, nullable=False)

    comments = db.relationship('Comment',backref='events')
    orders = db.relationship('Order', backref='events')

    

class Comment(db.Model):
    __tablename__='comments'

    id=db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, nullable=False)

    eventid=db.Column(db.Integer,db.ForeignKey('events.id'))
    userid=db.Column(db.Integer,db.ForeignKey('users.id'))

class Order(db.Model):
    __tablename__='orders'

    id=db.Column(db.Integer, primary_key=True)
    total=db.Column(db.Float, nullable=False)
    timebooked=db.Column(db.DateTime, nullable=False)

    eventid=db.Column(db.Integer,db.ForeignKey('events.id'))

    events = db.relationship('Event',backref='orders')

    
