# app/routes/__init__.py

from .auth_routes import auth
from .admin_routes import admin_routes
from .public_routes import public

def register_routes(app):
    app.register_blueprint(auth)
    app.register_blueprint(admin_routes)
    app.register_blueprint(public)
