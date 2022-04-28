import click
from flask import cli, current_app
from db import db
from users.service import create_user, get_user_by_email, set_admin
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


@click.command("add-admin")
@click.argument("email")
@cli.with_appcontext
def add_admin(email):
    user = get_user_by_email(email)
    # Check if user with given email exists
    if user is None:
        click.echo(f"User with email {email} not found!")
        return
    # Make user an admin
    set_admin(user.id, True)
    click.echo(f"User {email} is now an admin!")


@click.command("revoke-admin")
@click.argument("email")
@cli.with_appcontext
def revoke_admin(email):
    user = get_user_by_email(email)
    # Check if user with given email exists
    if user is None:
        click.echo(f"User with email {email} not found!")
        return
    # Revoke admin status from user
    set_admin(user.id, False)
    click.echo(f"User {email} is no longer an admin!")
