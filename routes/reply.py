from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.reply import Reply
from models.topic import Topic
from utils import log

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    log(u)
    if u is not None:
        r = Reply.new(form, user_id=u.id)
        t = Topic.find(r.topic_id)
        t.last_reply_time = r.created_time
        t.save()
        return redirect(url_for('topic.detail', id=r.topic_id))
    else:
        return redirect(url_for('index.index'))
