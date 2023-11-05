from boxtypev2 import *


# handles return statement control flow
# by only allowing function definition node
# to handle this exception

class ReturnException(Exception):
    def __init__(self, val):
        self.value = val  # replace with create_value(val)

    def __str__(self):
        return str(self.value)

    def get_val(self):
        return self.value


