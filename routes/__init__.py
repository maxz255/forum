from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from models.user import User
from functools import wraps


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


def admin_required():
    u = current_user()
    if u is None:
        return redirect('/')
    elif not u.is_admin():
        abort(404)


def login_required(func):
    @wraps(func)
    def _(*args, **kwargs):
        if current_user() is None:
            # return redirect(url_for('index.index'))
            return redirect('/')
        return func(*args, **kwargs)
    return _
