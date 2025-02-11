from iems.users.views import users_bp
from iems.auth.views import auth_bp
from iems.staffs.views import staff_bp
from iems.students.views import student_bp
from iems.parents.views import parent_bp
from iems.batch.views import batch_bp
from iems.semister.views import semister_bp
from iems.subjects.views import subjects_bp
from iems.courses.views import courses_bp
from iems.attendence.views import attendence_bp
from iems.leave.views import leave_bp
from iems.achievements.views import achievements_bp


def register_blueprints(app):
    app.blueprint(users_bp)
    app.blueprint(auth_bp)
    app.blueprint(staff_bp)
    app.blueprint(student_bp)
    app.blueprint(parent_bp)
    app.blueprint(batch_bp)
    app.blueprint(semister_bp)
    app.blueprint(subjects_bp)
    app.blueprint(courses_bp)
    app.blueprint(attendence_bp)
    app.blueprint(leave_bp)
    app.blueprint(achievements_bp)
