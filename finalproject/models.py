# import db object from flask app
from app import db

class users(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(100), unique = True, nullable = False)
   hash = db.Column(db.String, nullable = False)

def __init__(self, username, hash):
   self.username = username
   self.hash = hash