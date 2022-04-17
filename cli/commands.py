import click
from flask import cli, current_app
from db import db
from users.service import create_user
from products.service import create_product_category


@click.command("init-db")
@cli.with_appcontext
def init_db():
    # Drop all tables
    db.drop_all()
    click.echo("Dropped all database tables")
    # Create all tables
    db.create_all()
    click.echo("Created all database tables")
    # Create admin account
    config = current_app.config
    password = config["ADMIN_PASSWORD"]
    create_user("admin@shuBay.com", "ShuBay", "Admin", "123-456-7890", password, True)
    click.echo("Created admin account")
    # Create default product categories
    create_product_category("Food")
    create_product_category("Books")
    create_product_category("Fashion")
    create_product_category("Electronics")
    click.echo("Created default product categories")

