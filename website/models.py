# app/models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mood = db.relationship('MoodTracker')
    journal = db.relationship('JournalBersyukur')

    def get_id(self):
        return self.id
    
class MoodTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone = True), nullable=False, default = func.now())
    note = db.Column(db.String(100), nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class JournalBersyukur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(1000), nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))