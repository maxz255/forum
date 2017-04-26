from models import Model


class Board(Model):
    __fields__ = Model.__fields__ + [
        ('name', str, ''),
    ]
