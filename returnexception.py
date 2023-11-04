from boxtypev2 import *


class ReturnException(Exception):
    def __init__(self, val):
        self.value = create_value(val)

    def __str__(self):
        return str(self.value)

    def get_val(self):
        return self.value


