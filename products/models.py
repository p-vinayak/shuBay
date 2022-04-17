from db import db
from sqlalchemy import CheckConstraint


class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Numeric(8, 2), CheckConstraint('price > 0'), nullable=False, )
    stock = db.Column(db.Integer(), CheckConstraint('stock >= 0'), nullable=False)
    is_listed = db.Column(db.Boolean(), default=True, nullable=False)
    vendor_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer(), db.ForeignKey('product_category.id'))

    # Used internally, does not affect table creation
    vendor = db.relationship("User", foreign_keys=[vendor_id])
    category = db.relationship("ProductCategory", foreign_keys=[category_id])

    def __init__(self, name, description, price, stock, vendor_id, category_id, is_listed=True):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.vendor_id = vendor_id
        self.category_id = category_id
        self.is_listed = is_listed
