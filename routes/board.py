from flask import (
    request,
    redirect,
    url_for,
    render_template,
    Blueprint,
    abort,
)


from routes import admin_required
from models.board import Board

from utils import log

main = Blueprint('board', __name__)
main.before_request(admin_required)


@main.route('/admin')
def index():
        return render_template('board/admin_index.html')


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('topic.index'))


@main.route('/delete', methods=['POST'])
def delete():
    form = request.form
    name = form.get('name', '')
    m = Board.find_by(name=name)
    Board.delete(m)
    board_id = m.id
    # 同时把关联的topic删除
    from models.topic import Topic
    [Topic.delete(i) for i in Topic.find_all(board_id=board_id)]
    return redirect(url_for('topic.index'))
