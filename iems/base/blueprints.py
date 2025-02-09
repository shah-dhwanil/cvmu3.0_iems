from iems.users.views import users_bp
from iems.auth.views import auth_bp
from iems.staffs.views import staff_bp


def register_blueprints(app):
    app.blueprint(users_bp)
    app.blueprint(auth_bp)
    app.blueprint(staff_bp)
