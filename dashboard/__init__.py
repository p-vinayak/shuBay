from dashboard.controller import dashboard


def init_app(app):
    app.register_blueprint(dashboard)
