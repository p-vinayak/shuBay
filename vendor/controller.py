from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from vendor.service import *
from vendor.forms import VendorApplicationForm
from users.service import get_user_by_id, set_vendor

vendor = Blueprint("vendor", __name__, url_prefix="/vendor")


@vendor.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    # Redirect if users is already a vendor or has an active application
    if current_user.is_vendor or get_active_application_for_user(current_user.id) is not None:
        return redirect(url_for("dashboard.index"))
    # Create vendor application form
    form = VendorApplicationForm(request.form)
    # Create vendor application on valid form submission
    if form.validate_on_submit():
        create_vendor_application(current_user.id, form.title.data, form.description.data)
        return redirect(url_for("dashboard.index"))
    # Render vendor application page
    return render_template("vendor/apply.html", form=form, user=current_user)


@vendor.route("/applications", methods=["GET"])
@login_required
def applications():
    # Redirect if users is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    # Get all active applications and render applications page
    active_applications = get_all_active_applications()
    return render_template("vendor/applications.html", user=current_user, applications=active_applications)


@vendor.route("/applications/<int:id>", methods=["GET"])
@login_required
def application(id):
    # Redirect if users is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    application = get_application_by_id(id)
    # Redirect users if application doesn't exist or application has already been completed
    if application is None or not application.is_active:
        return redirect(url_for("dashboard.index"))
    # Render vendor application
    return render_template("vendor/application.html", user=current_user, application=application)


@vendor.route("/applications/<int:id>/approve", methods=["POST"])
@login_required
def approve_application(id):
    # Redirect if users is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    application = get_application_by_id(id)
    # Redirect users if application doesn't exist or application has already been completed
    if application is None or not application.is_active:
        return redirect(url_for("vendor.applications"))
    # Approve application and redirect to applications page
    complete_application(application.id, True, current_user.id)
    return redirect(url_for("vendor.applications"))


@vendor.route("/applications/<int:id>/deny", methods=["POST"])
@login_required
def deny_application(id):
    # Redirect if users is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    application = get_application_by_id(id)
    # Redirect users if application doesn't exist or application has already been completed
    if application is None or not application.is_active:
        return redirect(url_for("vendor.applications"))
    # Deny application and redirect to applications page
    complete_application(application.id, False, current_user.id)
    return redirect(url_for("vendor.applications"))


@vendor.route("/manage", methods=["GET"])
@login_required
def manage():
    # Redirect if user is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    vendors = get_all_vendors()
    # Render manage vendors page
    return render_template("vendor/manage.html", user=current_user, vendors=vendors)


@vendor.route("/manage/<int:id>", methods=["GET"])
@login_required
def manage_vendor(id):
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    user = get_user_by_id(id)
    # If user does not exist, redirect to vendor manage page
    if user is None:
        return redirect(url_for("vendor.manage"))
    # If user is not a vendor , redirect to vendor manage page
    if not user.is_vendor:
        return redirect(url_for("vendor.manage"))
    return render_template("vendor/manage_vendor.html", user=current_user, vendor=user)


@vendor.route("/manage/<int:id>/revoke", methods=["POST"])
@login_required
def revoke_vendor(id):
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    user = get_user_by_id(id)
    # If user does not exist, redirect to vendor manage page
    if user is None:
        return redirect(url_for("vendor.manage"))
    # If user is not a vendor , redirect to vendor manage page
    if not user.is_vendor:
        return redirect(url_for("vendor.manage"))
    set_vendor(user.id, False)
    return redirect(url_for("vendor.manage"))