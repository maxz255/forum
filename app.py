from flask import Flask
from routes.topic import main as topic_routes
from routes.index import main as index_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.mail import main as mail_routes
import markdown
import config


app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(board_routes, url_prefix='/board')
app.register_blueprint(mail_routes, url_prefix='/mail')


@app.context_processor
def include_markdown():
    return {'markdown': markdown}


@app.template_filter('format')
def format_time(unix_time):
    import time
    fmt = '%Y-%m-%d %H:%M'
    value = time.localtime(unix_time)
    dt = time.strftime(fmt, value)
    return dt


@app.template_filter('delta')
def time_delta(unix_time):
    import datetime
    now = datetime.datetime.now()
    past = datetime.datetime.fromtimestamp(unix_time)
    delta = now - past
    if delta.days != 0:
        return str(delta.days) + '天前'
    else:
        sec = delta.seconds
        if sec < 60:
            return str(sec) + '秒前'
        elif sec < 3600:
            return str(sec//60) + '分钟前'
        else:
            return str(sec//3600) + '小时前'


if __name__ == '__main__':
    app.run(**config.config)
