''' Contains User ORM classes for database table User '''

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.constants import *
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(500))
    time_taken = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    admin = db.Column(db.Boolean, default=False)

    def is_authenticated(self):
        return True
    
    def is_admin(self):
        return self.admin
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def set_password(self, password):
       self.password = generate_password_hash(password)
       
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.id)
    
    def __eq__(self, other):
        return self.id == other.id
