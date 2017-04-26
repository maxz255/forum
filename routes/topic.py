from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from utils import log

from routes import current_user
from routes import login_required

from models.topic import Topic
from models.board import Board
from models.user import User


main = Blueprint('topic', __name__)


@main.route('/')
def index():
    args = request.args
    board_id = int(args.get('board_id', -1))
    if board_id == -1:
        # ms = Topic.all()
        ts = Topic.cache_all()
    else:
        ts = Topic.find_all(board_id=board_id)
    bs = Board.all()
    return render_template('topic/index.html', ts=ts, bs=bs)


@main.route('/<int:id>')
def detail(id):
    t = Topic.get(id)
    b = Board.find(t.board_id)
    u = User.find(t.user_id)
    return render_template('/topic/detail.html', topic=t, board=b, user=u)


@main.route('/add', methods=['POST'])
@login_required
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    m.set_last_reply_time()
    return redirect(url_for('.detail', id=m.id))


@main.route('/new')
@login_required
def new():
    bs = Board.all()
    return render_template('topic/new.html', bs=bs)
