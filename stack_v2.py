class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1
        self.empty = True

    def push(self, element={}):
        self.stack.append(element)
        self.top += 1
        self.empty = False

    def update(self, index, var, val):
        self.stack[index][var] = val

    def pop(self):
        if not self.empty:
            if self.top == 0:
                self.empty = True
            top_val = self.stack.pop(self.top)
            self.top -= 1
            return top_val
        return None

    def find_var_scope(self, element):
        if not self.stack: # empty stack
            return None
        index = -1
        while index >= -len(self.stack):
            if element in self.stack[index]:
                return index
            index -= 1
        return None

    def top_index(self):
        return self.top

    def empty(self):
        return self.empty
