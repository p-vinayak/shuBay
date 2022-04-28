import json
from flask import Flask, redirect, url_for
from db import db
from cli.commands import init_db, add_admin, revoke_admin
from flask_login import LoginManager
from users.service import get_user_by_id
import auth
import dashboard
import vendor
import products
import cart
import orders


def create_app():
    app = Flask(__name__)

    # Load Config
    app.config.from_file("config.json", load=json.load)

    # Initialize DB
    db.init_app(app)

    # Initialize CLI commands
    app.cli.add_command(init_db)
    app.cli.add_command(add_admin)
    app.cli.add_command(revoke_admin)

    # Register routes
    auth.init_app(app)
    dashboard.init_app(app)
    vendor.init_app(app)
    products.init_app(app)
    cart.init_app(app)
    orders.init_app(app)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    # Load users on session fetch
    @login_manager.user_loader
    def user_loader(user_id):
        return get_user_by_id(user_id)

    # Home page should redirect to login page
    @app.route("/", methods=["GET", "POST"])
    def home():
        return redirect(url_for("auth.login"))

    return app
