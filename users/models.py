from flask_login import UserMixin
from db import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.Text(), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    password_plain = db.Column(db.Text(), nullable=False)
    is_vendor = db.Column(db.Boolean(), default=False ,nullable=False)
    is_admin = db.Column(db.Boolean(), default=False ,nullable=False)

    # Used internally, does not affect table creation
    cart = db.relationship("Cart", backref="user", lazy=False, uselist=False)

    def __init__(self, email, first_name, last_name, phone_number, password, password_plain):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.password_plain = password_plain
