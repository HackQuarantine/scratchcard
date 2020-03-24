from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask import request

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    student_status = db.Column(db.Boolean, default=False)
    # can they add / remove credits
    admin = db.Column(db.Boolean, default=False)
    claimed = db.relationship('Claimed', backref='user')
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
    def is_admin(self):
        return self.admin

# Credit refers to each type.
# We need to support:
# * Restrictions on status (i.e, are they are student)
# * Limit how many can be distributed
# * same code for everyone, or unique.

class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    unique = db.Column(db.Boolean) # whenever this the same code for everyone
    limit = db.Column(db.Integer) # How many can we give out
    student_only = db.Column(db.Boolean) # Is this for students only
    banner = db.Column(db.Text) # Banner image
    description = db.Column(db.Text) # Text description
    code = db.Column(db.Text) # used if it's a single code, otherwise NULL
    claimed = db.relationship('Claimed', backref='credit', cascade="all, delete, delete-orphan")
    tokens = db.relationship('Token', backref='credit', cascade="all, delete, delete-orphan")

# Track what each user has claimed.
class Claimed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey('credit.id'),
                     nullable=False)
    owner = db.Column(db.String(64), db.ForeignKey('user.id'),
        nullable=False)
    token = db.Column(db.Integer, db.ForeignKey('token.id'),
                      nullable=True)

# Allows users to claim unique codes
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Filter by owner to figure out how many are still left
    owner = db.Column(db.String(64), db.ForeignKey('user.id'),
        nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('credit.id'),
        nullable=False)
    code = db.Column(db.Text)

class OAuth(OAuthConsumerMixin, db.Model): pass
