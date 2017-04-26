from flask import (
    Blueprint,
    redirect,
    url_for,
    request,
    render_template
)

from models.mail import Mail
from models.user import User
from routes import current_user
from utils import log


main = Blueprint('main', __name__)


@main.route('/')
def index():
    u = current_user()
    r = Mail.find_all(receiver_id=u.id)
    s = Mail.find_all(sender_id=u.id)
    return render_template('mail/index.html', receives=r, sends=s)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    mail = Mail.new(form)
    mail.set_sender(u.id)
    return redirect(url_for('.index'))


@main.route('/detail/<int:id>')
def view(id):
    u = current_user()
    mail = Mail.find(id)

    # TODO 可以改进，让发送者看到“发送的私信”的detail时显示接收者，
    # TODO 看到“收到的私信”的detail时显示发送者
    if u.id == mail.receiver_id:
        mail.mark_read()
    if u.id in [mail.receiver_id, mail.sender_id]:
        sender = User.find(mail.sender_id)
        return render_template('mail/detail.html', mail=mail, u=sender)
    else:
        return redirect(url_for('.index'))
