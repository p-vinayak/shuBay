from vendor.controller import vendor


def init_app(app):
    app.register_blueprint(vendor)