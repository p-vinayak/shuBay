from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_required, current_user
from orders.service import *

orders = Blueprint("orders", __name__, url_prefix="/orders")


# Displays all past orders for a user
@orders.route("/", methods=["GET", "POST"])
@login_required
def index():
    orders = get_orders_for_user(current_user.id)
    # Render show all orders page
    return render_template("orders/index.html", user=current_user, orders=orders)


# Displays specific order details to user
@orders.route("/<int:id>", methods=["GET"])
@login_required
def order(id):
    order = get_order_by_id(id)
    # Redirect if order does not exist
    if order is None:
        flash("That order doesn't exist!", "danger")
        return redirect(url_for("orders.index"))
    # Redirect if user is not the owner of this order
    if order.customer_id != current_user.id:
        flash("You are not the creator of that order!", "danger")
        return redirect(url_for("orders.index"))
    # Render individual order page
    return render_template("orders/order.html", user=current_user, order=order)


# Gets all orders that need to be fulfilled or have been fulfilled, by this vendor
@orders.route("/requested", methods=["GET", "POST"])
@login_required
def requested():
    # Redirect if user is not a vendor
    if not current_user.is_vendor:
        flash("You are not a vendor!", "danger")
        return redirect(url_for("dashboard.index"))
    # Get all requested orders for vendor
    requested_orders = get_requested_orders(current_user.id)
    # Render requested orders page
    return render_template("orders/requested.html", user=current_user, requested_orders=requested_orders)


# Displays specific requested order to vendor. Allows them to fulfill the order and mark it as delivered
@orders.route("/requested/<int:order_id>/<int:product_id>", methods=["GET", "POST"])
@login_required
def requested_order_item(order_id, product_id):
    # Redirect if user is not a vendor
    if not current_user.is_vendor:
        flash("You are not a vendor!", "danger")
        return redirect(url_for("dashboard.index"))
    requested_order_item = get_requested_order(order_id, product_id, current_user.id)
    # Redirect user if no such requested order exists
    if requested_order_item is None:
        flash("No such requested order exists", "danger")
        return redirect(url_for("orders.requested"))
    # Complete order item if an order complete request was sent
    if request.method == "POST":
        # Redirect if order is already complete
        if requested_order_item.is_delivered:
            flash("Requested order is already completed!", "danger")
            return redirect(url_for("orders.requested"))
        complete_order_item(order_id, product_id)
        flash("Requested order successfully marked as completed!", "success")
        return redirect(url_for("orders.requested"))
    return render_template("orders/requested_order_item.html", user=current_user, requested_order_item=requested_order_item)