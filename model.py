from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(240), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()
