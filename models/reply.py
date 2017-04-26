from models import Model


class Reply(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('user_id', int, -1)
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    # def set_user_id(self, user_id):
    #     self.user_id = user_id
    #     self.save()
