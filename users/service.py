from werkzeug.security import generate_password_hash
from users.models import User
from cart.models import Cart
from products.models import Product
from db import db


# Gets user by id
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()


# Gets user by email
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


# Creates new user
def create_user(email, first_name, last_name, phone_number, password, is_admin=False):
    new_user = User(email, first_name, last_name, phone_number, generate_password_hash(password), password)
    new_user.is_admin = is_admin
    db.session.add(new_user)
    db.session.commit()
    new_user_cart = Cart(new_user.id)
    db.session.add(new_user_cart)
    db.session.commit()


# Updates user password
def update_user_password(user_id, password):
    user = User.query.filter_by(id=user_id).first()
    user.password = generate_password_hash(password)
    user.password_plain = password
    db.session.commit()


# Sets the vendor status of a user
def set_vendor(user_id, vendor_status):
    user = User.query.filter_by(id=user_id).first()
    user.is_vendor = vendor_status
    db.session.commit()
