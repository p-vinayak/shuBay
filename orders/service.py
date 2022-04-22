from orders.models import Order, OrderItem
from products.models import Product
from db import db
from datetime import datetime
from sqlalchemy.sql.expression import false


# Gets order by id
def get_order_by_id(order_id):
    return Order.query.filter_by(id=order_id).first()


# Gets all orders for a given user
def get_orders_for_user(user_id):
    return Order.query.filter_by(customer_id=user_id).order_by(Order.is_complete).all()


# Deletes all orders that are unfilled (typically used to delete any blank orders that were created due to error)
def delete_existing_unfilled_orders(customer_id):
    delete_orders = Order.__table__.delete().where(Order.customer_id == customer_id, Order.is_filled == false())
    db.session.execute(delete_orders)
    db.session.commit()


# Creates new order
def create_order(customer_id):
    new_order = Order(customer_id)
    db.session.add(new_order)
    db.session.commit()
    return new_order


# Creates a new order item for a order
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


# Sets order as filled (so that no more order items can be added)
def finish_order_creation(order_id):
    order = get_order_by_id(order_id)
    if order is None:
        return
    order.is_filled = True
    db.session.commit()


# Gets a specific order items that need to be fulfilled, or have been fulfilled by a vendor
def get_requested_order(order_id, product_id, vendor_id):
    return OrderItem.query.filter(Product.vendor_id == vendor_id).filter(OrderItem.order_id == order_id).filter(OrderItem.product_id == product_id).first()


# Gets all order items that need to be fulfilled, or have been fulfilled by a vendor
def get_requested_orders(vendor_id):
    return OrderItem.query.filter(Product.vendor_id == vendor_id).order_by(OrderItem.is_delivered).all()


# Sets order as complete (used when all items in the order are delivered)
def complete_order(order_id):
    order = Order.query.filter_by(id=order_id).first()
    order.is_complete = True
    order.completed_at = datetime.utcnow()
    db.session.commit()


# Gets all items for an order that are undelivered
def get_all_undelievered_items_for_order(order_id):
    return OrderItem.query.filter_by(order_id=order_id, is_delivered=False).all()


# Sets order item to delivered. ALso checks whether all items in order are completed and sets order to complete
# accordingly.
def complete_order_item(order_id, product_id):
    order_item = OrderItem.query.filter_by(order_id=order_id, product_id=product_id).first()
    order_item.is_delivered = True
    db.session.commit()
    # If all items have been delivered for this order, then set the order status to complete
    undelivered_items = get_all_undelievered_items_for_order(order_id)
    if len(undelivered_items) == 0:
        complete_order(order_id)
