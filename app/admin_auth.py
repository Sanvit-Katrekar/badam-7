''' Template Flask Auth Code '''

from flask import g, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView

class AuthModelView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AuthModelView, self).__init__(model, *args, **kwargs)

    def is_accessible(self):
        return g.user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))