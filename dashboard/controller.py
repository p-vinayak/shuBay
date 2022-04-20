from flask import Blueprint, render_template
from flask_login import login_required, current_user
from vendor.service import get_active_application_for_user

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# One-stop-shop for all functionalities on the website
@dashboard.route("/", methods=["GET"])
@login_required
def index():
    # Determine whether users has an active vendor application
    has_active_application = get_active_application_for_user(current_user.id) is not None
    return render_template("dashboard/index.html", user=current_user, has_active_application=has_active_application)
