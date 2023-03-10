from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db =SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_crreated = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)
    mhero = db.relationship('MarvelHero', backref = 'owner', lazy = True)

    def __init__(self, email, password, first_name = '', last_name = '',id = '', token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = self.set_token(24)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    def __repr__(self):
        return f"User {self.email} has been added to the database!"
        
class Hero(db.Model):
    id = db.Column(db.String(150), primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200))
    user_token=db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, name, description, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.user_token = user_token
    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"{self.name} has been added"

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description']

hero_schema = HeroSchema()
heroes_schema  = HeroSchema(many=True)

class MarvelHero(db.Model):
    id = db.Column(db.String(150), primary_key = True)
    marvel_id = db.Column(db.String(50))
    name = db.Column(db.String(150))
    description = db.Column(db.String())
    img = db.Column(db.String(150))
    user_token=db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, marvel_id, name, description ,img, user_token, id=''):
        self.id = self.set_id()
        self.marvel_id = marvel_id
        self.name = name
        self.description = description
        self.img = img
        self.user_token = user_token
        
    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"{self.name} has been added"

class marvelSchema(ma.Schema):
    class Meta:
        fields = ['id','marvel_id', 'name', 'description']


marvelhero_schema = marvelSchema()
marvelheroes_schema  = marvelSchema(many=True)


    