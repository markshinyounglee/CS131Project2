from intbase import *
from boxtypev2 import Value, create_value, get_printable


class EnvStack:
    def __init__(self):
        self.stack = []
        self.currScope = []  # contains the list of types of scopes
        self.top = 0
        self.empty = True
        self.error_reporter = InterpreterBase()

    def __find_var_scope(self, var):
        if not self.stack:  # empty stack
            return None
        index = -1
        while index >= -len(self.stack):
            if var in self.stack[index]:
                return index
            index -= 1
        return None

    def __push_element(self, var, val):  # enter new element to the topmost scope
        if self.empty:
            ## debugging code
            self.error_reporter.error(ErrorType.FAULT_ERROR,
                                      "ERROR: cannot push element to empty scope")
            ## delete after use
        self.stack[self.top - 1][var] = create_value(val)  # wrap val to wrapper class

    def push_params(self, var_val_dict):
        # when we declare a new function, formal parameters automatically
        # overshadow the previous variables
        # In this case, we want to push to the current scope no matter what
        # this is the only time when we declare new variables
        # despite already having variables with the same name

        # for sanity check, exit if we are not pushing the elements into an empty dictionary
        if self.stack[self.top - 1]:
            self.error_reporter.error(ErrorType.FAULT_ERROR,
                                      """Cannot push parameters when the current scope is nonempty""")
        for var, val in var_val_dict.items():
            self.stack[self.top - 1][var] = create_value(val)  # add value to stack directly so wrap it here

    # user will only "update" the variable and update() will take care of
    # it all
    def update(self, var_val_dict):
        if not self.stack:  # if stack is empty
            self.error_reporter.error(ErrorType.FAULT_ERROR,
                                      """No scope to update variables to""")
        else:
            for var, val in var_val_dict.items():
                var_scope = self.__find_var_scope(var)
                if var_scope is None:  # nonempty but not in any scope
                    self.__push_element(var, val)  # call __push_element() (val wrapped inside dunder method)
                else:  # update element in the nearest scope
                    self.stack[var_scope][var] = create_value(val)  # directly update the stack so wrap var

    def find_value_of_var(self, var):
        var_scope = self.__find_var_scope(var)
        if var_scope is None:
            self.error_reporter.error(
                ErrorType.NAME_ERROR, f"No variable named {var} in the current scope"
            )
        return self.stack[var_scope][var].value()  # unwrap

    def push_scope(self, scope_type):  # enter a new function scope
        self.stack.append({})
        self.top += 1
        self.empty = False
        if scope_type == InterpreterBase.FCALL_DEF:
            self.currScope.append(scope_type)  # mark the new scope as fcall
        elif scope_type in (InterpreterBase.IF_DEF, InterpreterBase.WHILE_DEF):
            self.currScope.append(scope_type)  # mark the new scope as if/while call
        else:
            self.error_reporter.error(ErrorType.FAULT_ERROR,
                                      "Invalid way to add another scope to the function")

    def pop(self):
        if not self.empty:
            if self.top == 1:
                self.empty = True
            top_val = self.stack.pop(self.top-1)
            top_scope = self.currScope.pop(self.top-1)
            self.top -= 1
            return {var:wrap_val.value() for var,wrap_val in top_val.items()}, top_scope
        return None

    def top_element(self):  # for inspection of the topmost scope purposes
        if self.empty:
            return None
        return {var:get_printable(wrapped_val) for var, wrapped_val in self.stack[self.top - 1].items()}

    def curr_scope(self):
        if self.empty:
            return None
        return self.currScope[self.top-1]

    def top_index(self):
        return self.top
        # points one above the last index element

    def empty(self):
        return self.empty
