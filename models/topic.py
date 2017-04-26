import json
from models import Model
import time


class Cache(object):

    def get(self, key):
        pass

    def set(self, key, value):
        pass


class MemoryCache(Cache):

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get(self, key):
        return RedisCache.redis_db.get(key)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)


class Topic(Model):
    # TODO 置顶功能，增加一个字段
    __fields__ = Model.__fields__ + [
        ('views', int, 0),
        ('title', str, ''),
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('last_reply_time', int, 0),
    ]

    should_update_all = True

    cache = RedisCache()
    # cache = MemoryCache()

    def save(self):
        super(Topic, self).save()
        Topic.should_update_all = True

    def to_dict(self):
        d = {}
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return d

    @classmethod
    def from_dict(cls, d):
        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        time.sleep(3)
        return Topic.all()

    @classmethod
    def cache_all(cls):
        if Topic.should_update_all:
            # 模拟调用all时有延迟的情况
            # Topic.cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            l = [i.to_dict() for i in cls.all()]
            Topic.cache.set('topic_all', json.dumps(l))
            Topic.should_update_all = False
        j = Topic.cache.get('topic_all').decode('utf-8')
        l = [Topic.from_dict(i) for i in json.loads(j)]
        return l

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        r = Reply.find_all(topic_id=self.id)
        return r

    def board(self):
        from .board import Board
        b = Board.find(self.board_id)
        return b

    def user(self):
        from .user import User
        u = User.find(id=self.user_id)
        return u

    def set_last_reply_time(self):
        self.last_reply_time = self.created_time
        self.save()
