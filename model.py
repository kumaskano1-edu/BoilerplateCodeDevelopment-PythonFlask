from flask import Flask
from sqlalchemy.dialects.postgresql import UUID
import uuid
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


ma = Marshmallow()
db = SQLAlchemy()
class Column(db.Model):
    __abstract__ = True
    def save(self):
        db.session.add(self)
        db.session.commit()          
class TraditionalAuth(Column):
    __tablename__ = 'traditional_auth'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
    def getId(self):
        return self.id
    @classmethod
    def find_by_email(self, email):
        return self.query.filter_by(email = email).first()
    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)    
class SocialAuth(Column):    
    __tablename__ = 'social_auth'
    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    social_id = db.Column(db.String(230), nullable=False, unique=True)
    provider_id = db.Column(db.Integer, nullable=False)
    provider_name = db.Column(db.String(100), nullable=False)
    def __init__(self, social_id, provider_id, provider_name):
        self.social_id = social_id
        self.provider_id = provider_id
        self.provider_name = provider_name
class User(Column):
    __tablename__ = 'users'
    id = db.Column(db.String(230), nullable=False, primary_key = True)
    name = db.Column(db.String(240), nullable=False)
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)
    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(id = id).first()
    def serialize(self):
        return {"id": str(self.id), "name": self.name}

