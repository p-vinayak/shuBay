from products.models import ProductCategory, Product
from cart.models import CartItem
from db import db
from sqlalchemy.sql.expression import true


# Creates a product category
def create_product_category(name):
    category = ProductCategory(name)
    db.session.add(category)
    db.session.commit()


# Gets all product categories
def get_all_product_categories():
    return ProductCategory.query.all()


# Creates a new product
def create_product(name, description, price, stock, vendor_id, category_id, is_listed):
    new_product = Product(name, description, price, stock, vendor_id, category_id, is_listed)
    db.session.add(new_product)
    db.session.commit()


# Gets all products that are listed and are purchasable
def get_product_listing():
    return Product.query.filter_by(is_listed=True).filter(Product.stock > 0).all()


# Gets product by id
def get_product_by_id(product_id):
    return Product.query.filter_by(id=product_id).first()


# Updates product details
def update_product(product_id, price, stock, category_id, is_listed):
    product = Product.query.filter_by(id=product_id).first()
    product.price = price
    product.stock = stock
    product.category_id = category_id
    product.is_listed = is_listed
    if not product.is_listed:
        delete_cart_items = CartItem.__table__.delete().where(CartItem.product_id == product.id, Product.is_listed == true())
        db.session.execute(delete_cart_items)
    db.session.commit()


# Gets all products owned by a vendor
def get_products_by_vendor(vendor_id):
    return Product.query.filter_by(id=vendor_id).all()

