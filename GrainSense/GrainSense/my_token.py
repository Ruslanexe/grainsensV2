import random
import string
import datetime
from sortedcontainers import SortedSet

MAX_USERS_AMOUNT = 0b11111111
TOKEN_LENGTH = 0b10000

used_token_names = SortedSet()
active_tokens = SortedSet()


def expiration_time(time):
    return time + datetime.timedelta(minutes=30)


class AccessToken:
    def __init__(self, user_id, token=None, expires=None):
        if token:
            self.value = token
        else:
            self.value = ''.join(random.choice(string.ascii_letters) for _ in range(TOKEN_LENGTH))
            while self.value in used_token_names:
                self.value = ''.join(random.choice(string.ascii_letters) for _ in range(TOKEN_LENGTH))

        if expires:
            self.expires = expires
        else:
            self.expires = expiration_time(datetime.datetime.now().replace(microsecond=0))

        self.user = user_id

    def __eq__(self, other):
        return self.value == other.value and self.expires == other.expires and self.user == other.user

    def __lt__(self, other):
        if self.expires < other.expires:
            return True
        elif self.expires == other.expires:
            if self.value < other.value:
                return True
            elif self.value == other.value:
                return self.user < other.user
            else:
                return False
        return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __hash__(self):
        return hash(str(self.expires) + self.value + str(self.user))

    def __str__(self):
        return '{' + f"user: {self.user}, token: {self.value}, expires: {str(self.expires)}" + '}'

    def validate(self):
        used_token_names.add(self.value)
        active_tokens.add(self)


def remove_old_tokens():
    while len(active_tokens) > 0 and active_tokens[0].expires <= datetime.datetime.now().replace(microsecond=0):
        used_token_names.remove(active_tokens[0].value)
        active_tokens.remove(active_tokens[0])

