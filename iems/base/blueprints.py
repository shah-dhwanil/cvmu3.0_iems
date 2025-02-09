from iems.users.views import users_bp

def register_blueprints(app):
    app.blueprint(users_bp)