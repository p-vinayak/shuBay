from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user, login_required
from products.forms import CreateProductCategoryForm, CreateProductForm, UpdateProductForm
from products.service import *
from cart.service import *
from products.forms import AddProductToCartForm

products = Blueprint("products", __name__, url_prefix="/products")


# Allows admins to create product categories
@products.route("/category/create", methods=["GET", "POST"])
@login_required
def create_category():
    # Redirect if users is not an admin
    if not current_user.is_admin:
        return redirect(url_for("dashboard.index"))
    # Initialize create product category form
    form = CreateProductCategoryForm(request.form)
    # Create product category if form is valid on submission
    if form.validate_on_submit():
        create_product_category(form.category_name.data)
        return redirect(url_for("dashboard.index"))
    # Render create product category page
    return render_template("products/create_category.html", user=current_user, form=form)


# Allows vendors to create new products
@products.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # Redirect if users is not a vendor
    if not current_user.is_vendor:
        return redirect(url_for("dashboard.index"))
    # Initialize create product form
    form = CreateProductForm(request.form)
    # Populate product category select field with values from DB
    form.category.choices = [(category.id, category.name) for category in get_all_product_categories()]
    # Create product if form is valid on submit
    if form.validate_on_submit():
        create_product(form.name.data, form.description.data, form.price.data, form.stock.data, current_user.id,
                       form.category.data, form.is_listed.data)
        return redirect(url_for("dashboard.index"))
    return render_template("products/create_product.html", user=current_user, form=form)


# Allows vendors to manage specific products that are owned by them
@products.route("/manage/<int:id>", methods=["GET", "POST"])
@login_required
def manage_product(id):
    # Redirect if user is not a vendor
    if not current_user.is_vendor:
        return redirect(url_for("dashboard.index"))
    # Redirect if product does not exist
    product = get_product_by_id(id)
    if product is None:
        return redirect(url_for("products.manage"))
    # Redirect if vendor is not the owner of this product
    if product.vendor.id != current_user.id:
        return redirect(url_for("products.manage"))
    # Initialize create product form
    form = UpdateProductForm(request.form)
    # Populate product category select field with values from DB
    form.category.choices = [(category.id, category.name) for category in get_all_product_categories()]
    # Update product if form is valid on submit
    if form.validate_on_submit():
        update_product(product.id, form.price.data, form.stock.data, form.category.data, form.is_listed.data)
        return redirect(url_for("products.manage_product", id=product.id))
    # Update form default values using existing product values
    form.price.default = product.price
    form.stock.default = product.stock
    form.category.default = product.category_id
    form.is_listed.render_kw['checked'] = product.is_listed
    form.process()
    # Render manage product page
    return render_template("products/manage_product.html", user=current_user, form=form, product=product)


# Allows vendors to see all products owned by them
@products.route("/manage", methods=["GET"])
@login_required
def manage():
    # Redirect if user is not a vendor
    if not current_user.is_vendor:
        return redirect(url_for("dashboard.index"))
    # Get all products owned by vendor, listed or not
    products = get_products_by_vendor(current_user.id)
    # Render manage products page
    return render_template("products/manage.html", user=current_user, products=products)


# Lists all products that are listed and have stock
@products.route("/", methods=["GET"])
@login_required
def index():
    # Get all listed products that are currently in stock
    products = get_product_listing()
    # Render product listing page
    return render_template("products/index.html", user=current_user, products=products)


# Displays a specific product that can be purchased
@products.route("/product/<int:id>", methods=["GET", "POST"])
@login_required
def product(id):
    product = get_product_by_id(id)
    # Redirect if product doesn't exist
    if product is None:
        return redirect(url_for("products.index"))
    # Redirect if product is not listed or has no stock available
    if not product.is_listed or product.stock < 1:
        return redirect(url_for("products.index"))
    # Get this product as a cart item, if the user has it in their cart
    cart_item = get_cart_item(current_user.cart.id, product.id)
    # Initialize add product to cart form
    form = AddProductToCartForm(request.form, product_id=product.id)
    # Add product to cart on valid form submission
    if form.validate_on_submit():
        # Redirect if product is already in the user's cart
        # Any updates to cart item or purchase quantity should be handled in the cart route
        if cart_item is not None:
            return redirect(url_for("products.index"))
        create_cart_item(current_user.cart.id, product.id, form.item_count.data)
        return redirect(url_for("products.index"))
    # Render product page
    # Do not render add product to cart form if user already has this product in their cart
    # The page will instead render a message asking the user to go to their cart to make any updates
    return render_template("products/product.html", user=current_user, product=product, cart_item=cart_item,
                           form=form if cart_item is None else None)
