from orders.models import Order, OrderItem
from products.models import Product
from db import db
from datetime import datetime
from sqlalchemy.sql.expression import false


def get_order_by_id(order_id):
    return Order.query.filter_by(id=order_id).first()


def get_orders_for_user(user_id):
    return Order.query.filter_by(customer_id=user_id).all()


def delete_existing_unfilled_orders(customer_id):
    delete_orders = Order.__table__.delete().where(Order.customer_id == customer_id, Order.is_filled == false())
    db.session.execute(delete_orders)
    db.session.commit()


def create_order(customer_id):
    new_order = Order(customer_id)
    db.session.add(new_order)
    db.session.commit()
    return new_order


def create_order_item(order_id, product_id, price, quantity, sub_total):
    order = get_order_by_id(order_id)
    product = Product.query.filter_by(id=product_id).first()
    # If given order or product don't exist, exit early
    if order is None or product is None:
        return
    # Don't add item to order if order is already fully filled
    if order.is_filled:
        return
    # If purchase quantity exceeds product stock for any reason at this point (this should never happen on this method)
    # Set purchase quantity to product stock
    if quantity > product.stock:
        quantity = product.stock
    new_order_item = OrderItem(order_id, product_id, price, quantity, sub_total)
    db.session.add(new_order_item)
    product.stock -= quantity
    db.session.commit()
    order.sub_total = order.calculate_sub_total()
    order.delivery_charge = order.calculate_delivery_charge()
    order.taxes = order.calculate_taxes()
    order.total = order.calculate_total()
    db.session.commit()


def finish_order_creation(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return
    order.is_filled = True
    db.session.commit()


def get_requested_order(order_id, product_id, vendor_id):
    return OrderItem.query.filter(Product.vendor_id == vendor_id).filter(OrderItem.order_id == order_id).filter(OrderItem.product_id == product_id).first()


def get_requested_orders(vendor_id):
    return OrderItem.query.filter(Product.vendor_id == vendor_id).all()


def complete_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    order.is_complete = True
    order.completed_at = datetime.utcnow()
    db.session.commit()


def get_all_undelievered_items_for_order(order_id):
    return OrderItem.query.filter_by(order_id=order_id, is_delivered=False).all()


def complete_order_item(order_id, product_id):
    order_item = OrderItem.query.filter_by(order_id=order_id, product_id=product_id).first()
    order_item.is_delivered = True
    db.session.commit()
    # If all items have been delivered for this order, then set the order status to complete
    undelivered_items = get_all_undelievered_items_for_order(order_id)
    if len(undelivered_items) == 0:
        complete_order(order_id)
