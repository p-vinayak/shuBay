from auth.controller import auth


def init_app(app):
    app.register_blueprint(auth)