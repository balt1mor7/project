import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for, current_app
from app import db


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self) -> str:
        return ' '.join([self.last_name,
                         self.first_name,
                         self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login


class Auction(db.Model):

    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    place = db.Column(db.Text)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self) -> str:
        return '<Auction %r>' % self.description


class Item(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey(
        "auctions.id"), nullable=False)
    lot_number = db.Column(db.String(100), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    starting_price = db.Column(db.Integer, nullable=False)
    short_desc = db.Column(db.Text)
    date_of_sale = db.Column(db.Date, default=None)
    sale_price = db.Column(db.Integer, default=None)
    buyer_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"))

    auction = db.relationship('Auction')
    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])

    def __repr__(self) -> str:
        return '<Item %r>' % self.short_desc
