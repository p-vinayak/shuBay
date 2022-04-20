from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from cart.service import get_cart_item, delete_cart_item, update_cart_item_quantity, adjust_cart_item, clear_cart
from cart.forms import UpdateCartItem
from orders.service import *

cart = Blueprint("cart", __name__, url_prefix="/cart")


# Displays all cart items to user
@cart.route("/", methods=["GET"])
@login_required
def index():
    # Adjust cart items' purchase quantity if purchase quantity is no longer available
    for item in current_user.cart.items:
        if item.quantity > item.product.stock:
            adjust_cart_item(current_user.cart.id, item.product.id)
            item.is_adjusted = True
    # Render cart page
    return render_template("cart/index.html", user=current_user, cart_items=current_user.cart.items)


# Allows user to manage individual cart item
@cart.route("/manage/<int:id>", methods=["GET", "POST"])
@login_required
def manage(id):
    cart_item = get_cart_item(current_user.cart.id, id)
    # Redirect user if cart item doesn't exist
    if cart_item is None:
        return redirect(url_for("cart.index"))
    # Delete cart item if product is not listed anymore and redirect user
    if not cart_item.product.is_listed:
        delete_cart_item(current_user.cart.id, cart_item.product.id)
        return redirect(url_for("cart.index"))
    # Adjust cart item's purchase quantity if purchase quantity is no longer available
    if cart_item.quantity > cart_item.product.stock:
        adjust_cart_item(current_user.cart.id, cart_item.product.id)
        cart_item.is_adjusted = True
    # Initialize update cart item form
    form = UpdateCartItem(request.form, product_id=cart_item.product.id)
    # Update cart item on valid form submission
    if form.validate_on_submit():
        update_cart_item_quantity(current_user.cart.id, id, form.item_count.data)
        return redirect(url_for("cart.manage", id=id))
    # Set form item count default value to current purchase quantity of cart item
    form.item_count.default = cart_item.quantity
    form.process()
    # Render manage cart item page
    return render_template("cart/manage.html", user=current_user, item=cart_item, form=form)


# Removes specific product from cart
@cart.route("manage/<int:id>/remove", methods=["GET", "POST"])
@login_required
def remove(id):
    delete_cart_item(current_user.cart.id, id)
    return redirect(url_for("cart.index"))


# Checks out all items in cart and creates an order from it
@cart.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    # Adjust cart items' purchase quantity if purchase quantity is no longer available
    for item in current_user.cart.items:
        if item.quantity > item.product.stock:
            adjust_cart_item(current_user.cart.id, item.product.id)
            item.is_adjusted = True
    # On checkout, create order
    if request.method == "POST":
        # Redirect if cart has no items. No order should be created.
        if len(current_user.cart.items) < 1:
            return redirect(url_for("cart.checkout"))
        # If any blank orders were created in the past due to errors, delete them
        delete_existing_unfilled_orders(current_user.id)
        # Create new blank order
        new_order = create_order(current_user.id)
        # Create order items for created blank order
        for item in current_user.cart.items:
            create_order_item(new_order.id, item.product.id, item.product.price, item.quantity, item.calculate_sub_total())
        # Set order status to filled, meaning no more order items can be added to this order
        finish_order_creation(new_order.id)
        clear_cart(current_user.cart.id)
        return redirect(url_for("orders.index"))
    return render_template("cart/checkout.html", user=current_user, cart_items=current_user.cart.items,
                           delivery_charge=current_user.cart.calculate_delivery_charge(),
                           taxes=current_user.cart.calculate_taxes(),
                           sub_total=current_user.cart.calculate_sub_total(),
                           total=current_user.cart.calculate_total())