from cart.models import CartItem
from db import db


# Creates new cart item
def create_cart_item(cart_id, product_id, quantity):
    new_cart_item = CartItem(cart_id, product_id, quantity)
    db.session.add(new_cart_item)
    db.session.commit()


# Gets cart item by cart id and product id
def get_cart_item(cart_id, product_id):
    return CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()


# Deletes cart item from a cart
def delete_cart_item(cart_id, product_id):
    cart_item = get_cart_item(cart_id, product_id)
    if cart_item is None:
        return
    db.session.delete(cart_item)
    db.session.commit()


# Adjusts purchase quantity for cart item to match available stock
def adjust_cart_item(cart_id, product_id):
    cart_item = get_cart_item(cart_id, product_id)
    if cart_item is None:
        return
    cart_item.quantity = cart_item.product.stock
    db.session.commit()


# Updates cart item purchase quantity with new quantity
def update_cart_item_quantity(cart_id, product_id, new_quantity):
    cart_item = get_cart_item(cart_id, product_id)
    if cart_item is None:
        return
    cart_item.quantity = new_quantity
    db.session.commit()


# Removes all cart items from a cart
def clear_cart(cart_id):
    delete_query = CartItem.__table__.delete().where(CartItem.cart_id == cart_id)
    db.session.execute(delete_query)
    db.session.commit()
