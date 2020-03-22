from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask import request

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id

# Credit refers to each type. 
class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    unique = db.Column(db.Boolean) # whenever this the same code for everyone
    # type
#    name
    banner = db.Column(db.Text) # Banner image

# A valid token. 
# Can only be claimed by one user.
#class Token(db.Model):
#    pass

class OAuth(OAuthConsumerMixin, db.Model): pass
