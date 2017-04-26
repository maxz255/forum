from models import Model


class User(Model):
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
        # 11代表普通用户, 1代表管理员
        ('role', str, 11)
    ]

    def salted_password(self, password, salt='*&!>o8r9<fi1438A($%Qhy'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib

        p = pwd.encode('ascii')
        s = hashlib.sha256(p)

        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        # 这里是不是没必要这样做，直接username = form.get('username', '')，
        # password = form.get('password', '') ?
        u = User()
        u.username = form.get('username', '')
        u.password = form.get('password', '')
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    def is_admin(self):
        return self.role == 1
