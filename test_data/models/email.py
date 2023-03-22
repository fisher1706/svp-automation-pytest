class Email:  # pylint: disable=too-few-public-methods

    def __init__(self, _from, _to, date, subject, body):
        self._from = _from
        self._to = _to
        self.date = date
        self.subject = subject
        self.body = body
