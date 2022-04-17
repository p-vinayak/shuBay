from db import db
from sqlalchemy import func, CheckConstraint
from decimal import Decimal


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer(), primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    is_complete = db.Column(db.Boolean(), default=False, nullable=False)
    is_filled = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=False), server_default=func.now(), nullable=False)
    completed_at = db.Column(db.DateTime(timezone=False), nullable=True)
    delivery_charge = db.Column(db.Numeric(8, 2), CheckConstraint("delivery_charge >= 0"), default=0, nullable=False)
    taxes = db.Column(db.Numeric(8, 2), CheckConstraint("taxes >= 0"), default=0, nullable=False)
    sub_total = db.Column(db.Numeric(8, 2), CheckConstraint("sub_total >= 0"), default=0, nullable=False)
    total = db.Column(db.Numeric(8, 2), CheckConstraint("total >= 0"), default=0, nullable=False)

    # Used internally, does not affect table creation
    items = db.relationship("OrderItem", lazy=False, backref="order", cascade="all,delete")

    def __init__(self, customer_id):
        self.customer_id = customer_id

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


class OrderItem(db.Model):
    __tablename__ = "order_item"

    order_id = db.Column(db.Integer(), db.ForeignKey("order.id"), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False, primary_key=True)
    product_price = db.Column(db.Numeric(8, 2), CheckConstraint("product_price >= 0"), nullable=0)
    product_quantity = db.Column(db.Integer(), CheckConstraint("product_quantity > 0"), nullable=False)
    sub_total = db.Column(db.Numeric(8, 2), CheckConstraint("sub_total >= 0"), nullable=False)
    is_delivered = db.Column(db.Boolean(), default=False, nullable=False)

    # Used internally, does not affect table creation
    product = db.relationship("Product", foreign_keys=[product_id])

    def calculate_sub_total(self):
        return self.product_quantity * self.product_price

    def __init__(self, order_id, product_id, price, quantity, sub_total):
        self.order_id = order_id
        self.product_id = product_id
        self.product_price = price
        self.product_quantity = quantity
        self.sub_total = sub_total
