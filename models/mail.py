from models import Model


class Mail(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
        ('read', bool, False),
    ]

    def mark_read(self):
        self.read = True
        self.save()

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()
