from cart.controller import cart


def init_app(app):
    app.register_blueprint(cart)