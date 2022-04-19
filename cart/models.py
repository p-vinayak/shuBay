from db import db
from sqlalchemy import CheckConstraint
from decimal import Decimal


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    # Used internally, does not affect table creation
    items = db.relationship("CartItem", lazy=False, backref="cart")

    def calculate_delivery_charge(self):
        # $1.50 per item
        return round(len(self.items) * Decimal('1.50'), 2)

    def calculate_sub_total(self):
        sub_total = Decimal('0.00')
        for item in self.items:
            sub_total += item.calculate_sub_total()
        return sub_total

    def calculate_taxes(self):
        # 20% of total cost
        return round((self.calculate_sub_total() + self.calculate_delivery_charge()) * Decimal('0.20'), 2)

    def calculate_total(self):
        return round(self.calculate_sub_total() + self.calculate_taxes() + self.calculate_delivery_charge(), 2)

    def __init__(self, owner_id):
        self.owner_id = owner_id


class CartItem(db.Model):
    __tablename__ = "cart_item"

    cart_id = db.Column(db.Integer(), db.ForeignKey("cart.id", ondelete="CASCADE"), nullable=False, primary_key=True, autoincrement=False)
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False, primary_key=True, autoincrement=False)
    quantity = db.Column(db.Integer(), CheckConstraint("quantity > 0"), nullable=False)

    # Used internally, does not affect table creation
    product = db.relationship("Product", lazy=False, backref="cart_item", uselist=False)
    is_adjusted = False

    def calculate_sub_total(self):
        return round(self.product.price * self.quantity, 2)

    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    def needs_adjusting(self):
        return self.product.stock < self.quantity
