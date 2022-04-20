from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required, logout_user
from auth.forms import RegistrationForm, LoginForm, UpdatePasswordForm
from users.service import create_user, get_user_by_email, update_user_password
from flask_login import login_user

auth = Blueprint("auth", __name__, url_prefix="/auth")


# User registration
@auth.route("/register", methods=["GET", "POST"])
def register():
    # Redirect to dashboard if users already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    # Create registration form
    form = RegistrationForm(request.form)
    # Create users on valid form submission
    if form.validate_on_submit():
        create_user(form.email.data, form.first_name.data, form.last_name.data, form.phone_number.data, form.password.data)
        return redirect(url_for("auth.login"))
    # Render registration page
    return render_template("auth/register.html", form=form)


# User login
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Redirect to dashboard if users already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    # Create login form
    form = LoginForm(request.form)
    # Login users on valid form submission
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        login_user(user)
        return redirect(url_for("dashboard.index"))
    # Render login page
    return render_template("auth/login.html", form=form)


# User logout
@auth.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Password change. Logouts out user on password change.
@auth.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    # Initialize update password form
    form = UpdatePasswordForm(request.form, user_id=current_user.id)
    # Update password on valid form submission
    if form.validate_on_submit():
        update_user_password(current_user.id, form.new_password.data)
        # Logout user so they have to re-login with their new password
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template("auth/update_password.html", form=form)
