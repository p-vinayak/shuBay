from products.controller import products


def init_app(app):
    app.register_blueprint(products)
