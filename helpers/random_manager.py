import string
from random import randint, choices


class RandomManager:

    @staticmethod
    def _random_int(size):
        range_start = 10 ** (size - 1)
        range_end = (10 ** size) - 1
        return randint(range_start, range_end)

    @staticmethod
    def random_alphanumeric(size):
        return ''.join(choices(string.ascii_letters + string.digits, k=size))

    @staticmethod
    def random_letters(size):
        return ''.join(choices(string.ascii_letters, k=size))

    def random_name(self):
        return f"Autotest {self.random_letters(8).lower()}"

    def random_email(self, personal_number=None, domain="qa.qiwa.tech", prefix='auto'):
        if not personal_number:
            personal_number = self.random_alphanumeric(8).lower()
        return f"{prefix}-{personal_number}@{domain}"

    def random_number(self, size=9, prefix=''):
        return f"{prefix}{self._random_int(size)}"
