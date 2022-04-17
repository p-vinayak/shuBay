from orders.controller import orders


def init_app(app):
    app.register_blueprint(orders)