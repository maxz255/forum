from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)
from config import user_file_directory
from models.user import User
from werkzeug.utils import secure_filename
import os.path
from utils import log
from routes import login_required
from routes import current_user

main = Blueprint('index', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('topic.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('topic.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
@login_required
def profile():
        u = current_user()
        return render_template('profile.html', user=u)


def allow_file(filename):
    from config import accept_user_file_type
    suffix = filename.split('.')[-1]
    return suffix in accept_user_file_type


# TODO filename应该弄成随机不重复的文件名
@main.route('/addimg', methods=['POST'])
@login_required
def add_img():
    if 'file' not in request.files:
        return redirect(url_for('.profile'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('.profile'))

    if allow_file(file.filename):
        u = current_user()
        filename = secure_filename(file.filename)
        path = os.path.join(user_file_directory, filename)
        file.save(path)
        u.user_image = filename
        u.save()

    return redirect(url_for('.profile'))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_directory, filename)
