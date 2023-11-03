# TO BE TURNED IN #
from intbase import *  # import class from module
from brewparse import parse_program
from stackv2 import EnvStack
import copy  # return statement should return deep copy


# In Python, it is helpful to add a box type (wrapper class)
# to restrict the operations a type is allowed to perform
# And I know exactly what operators can be used
# Store values in a wrapper class and check the types manually
# if you store types consistently and use lambdas, there is a simple
# way to implement all the operations

# implement logic to pass the arguments in run_func
# which implements func node or function definition node.
# Then, you can implement evaluate_func_call_expression
# and run_func_call.
# Then, you should implement the dynamic scoping logic.
# Then, test your code, and hopefully you are done.


class Interpreter(InterpreterBase):  # TO DO
    def __init__(self, console_output=True, inp=None,
                 trace_output=False):
        super().__init__(console_output, inp)
        # console_output determines where to direct output
        # inp needed for automated testing only
        # trace_output is for debugging purposes
        self.trace_output = trace_output
        # insert more code as needed
        # any method can add member variables
        # TO DO: replace variable_name_to_values to var_value_stack
        # This is used for project 1; not for project 2
        # self.variable_name_to_value = {}
        # map to hold all values to variables
        self.var_value_stack = EnvStack()
        # stack of dictionaries that map variable to value (for dynamic scoping)
        # var_value_stack = [block1: [x:10, y:1], block2: [y:1, z:true]] <- top
        self.func_arg_dict = {}
        # any custom function declarations and list of number of parameters
        # function name maps to a dictionary of
        # (num-of-parameters):(index-of-function-definition-in-astree.dict['functions']).
        # func_arg_dict = {func1:{2:0, 1:1, 0:3}, func2:{3:2}, func3:{4:4}, ...}
        self.func_node_list = None  # access astree.dict['functions']
        # alias to astree.dict['functions']
        # READ ONLY

    def run(self, program):  # TO DO
        # program is an array of program strings
        # refer to pages 7-8 for pseudocode
        astree = parse_program(program)  # root node
        # returns tree with Element-type nodes
        # TO DO: traverse the tree and evaluate the semantics

        # debugging code
        # super().output(astree)
        # delete after use

        if astree.elem_type != 'program':
            super().error(ErrorType.NAME_ERROR,
                          "No program node found")

        self.func_node_list = astree.dict['functions']
        main_found = False
        main_node = None
        index = 0
        for function in astree.dict['functions']:  # see if main() exists
            function_name = function.dict['name']
            argument_count = len(function.dict['args'])
            # check if the function has no overloaded functions
            if function_name not in self.func_arg_dict:
                # number of arguments:index in astree.dict['functions']
                self.func_arg_dict[function_name] = {argument_count: index}
            # check if no function signature overlaps
            elif argument_count not in self.func_arg_dict[function_name]:
                # add new index with that function signature
                self.func_arg_dict[function_name][argument_count] = index
            # if signatures overlap, return an error
            else:
                super().error(ErrorType.NAME_ERROR, """Two conflicting function 
                                                    signature detected""")

            if function_name == 'main':
                main_found = True
                main_node = function
            index += 1
        if not main_found:
            super().error(ErrorType.NAME_ERROR, """The program
                        does not start with the main() function""")
        else:
            # always create scope before running function declaration
            # main takes no parameters, so we don't need to push any formal parameters
            self.var_value_stack.push_scope(InterpreterBase.FCALL_DEF)
            self.run_func(main_node)  # run the function from func node "main" (type Element)
            self.var_value_stack.pop()

    ## FIX THIS! with dynamic scoping
    # strategy: have a stack of dictionaries that list all the elements in that scope
    # this would facilitate the variable lifetime control (popping the stack deletes all variables)
    # as well as accessing the variables of the nearest enclosing scope
    def run_func(self, func_node):  # execute statements (for function definition node (func node))
        # for project 2, function definition nodes dict['args'] = list of Argument nodes (formal parameters)
        # we should ensure that formal parameters shadow all other global-scope values in dynamic scoping

        # if function is custom, push all the formal parameter and their passed values to stack
        # push all formal parameters passed in into the stack

        # this could be done when run_func_call is invoked

        # run all statements
        self.run_statement_block(func_node.dict['statements'])

        # pushing and popping the scope handled by run_func_call

    def run_statement_block(self, statement_list):
        for statement in statement_list:
            self.run_statement(statement)

    def run_statement(self, statement_node):  # fork to assignment or fcall
        if statement_node.elem_type == '=':
            self.run_assignment(statement_node)
        elif statement_node.elem_type == 'fcall':
            self.run_func_call(statement_node)
        elif statement_node.elem_type == 'if':
            self.run_if_call(statement_node)
        elif statement_node.elem_type == 'while':
            self.run_while_call(statement_node)
        elif statement_node.elem_type == 'return':
            self.run_return_call(statement_node)
        else:
            super().error(ErrorType.NAME_ERROR, """
            The statement is neither assignment 
            nor function""")

    def run_assignment(self, statement_node):  # run assignment statement node
        target_var_name = statement_node.dict['name']
        expression_name = statement_node.dict['expression']  # maps to expression node
        expression_value = self.evaluate_expression(expression_name)
        # either add the var-val pair to the nearest scope or update the nearest enclosing scope var
        self.var_value_stack.update({target_var_name: expression_value})

    def run_func_call(self, statement_node):  # run fcall statement node
        # for project 2, print() and custom functions are both valid function call statements
        # and run_func_call always returns a value, nil or actual
        function_name = statement_node.dict['name']
        if function_name in ('print', 'inputi', 'inputs'):  # standard functions we defined
            self.evaluate_func_call_expression(statement_node)  # have all the same components
        elif function_name in self.func_arg_dict:
            # if the function name is defined, check if parameter count is correct
            # func_arg_dict maps to a list of possible number of parameters
            arg_len = len(statement_node.dict['args'])
            if arg_len in self.func_arg_dict[function_name]:
                # if yes, then execute that function with the given argument list
                func_index = self.func_arg_dict[function_name][arg_len]
                formal_arg_list = self.func_node_list[func_index].dict['args']
                # pushed all necessary variables in the stack
                self.var_value_stack.push_scope(InterpreterBase.FCALL_DEF)
                self.var_value_stack.push_params({arg_name.dict['name']: self.evaluate_expression(arg_val)
                                                  for arg_name, arg_val in
                                                  zip(formal_arg_list, statement_node.dict['args'])})
                # call the function definition node
                self.run_func(self.func_node_list[func_index])
                # exit current scope
                self.var_value_stack.pop()
            else:
                # if no, then throw NAME_ERROR
                super().error(ErrorType.NAME_ERROR,
                              f"No function {statement_node.dict['name']} with {len(statement_node.dict['args'])} arguments")
        else:
            super().error(ErrorType.NAME_ERROR,
                          f"{statement_node.dict['name']} is not a valid function statement")
        """
        recall that only function used as a statement is
        print, which uses super().output()

        In the future, this may have to return value
        but for now, we don't have to return anything
        """

    # proposition: if, while, and return can all be thought of as function definition node
    def run_if_call(self, statement_node):
        ## debugging code
        if statement_node.elem_type != 'if':
            super().error(ErrorType.FAULT_ERROR, "not an if statement")
        ## delete after use

        # dict['condition'] contains expression to be evaluated
        # create new scope
        self.var_value_stack.push_scope(InterpreterBase.IF_DEF)
        condition = self.evaluate_expression(statement_node.dict['condition'])
        if not isinstance(condition, bool):
            super().error(ErrorType.TYPE_ERROR,
                          """The if condition does not evaluate to boolean value""")
        elif condition:
            self.run_statement_block(statement_node.dict['statements'])
        else:  # no else-if branching
            if statement_node.dict['else_statements'] is not None:  # check if else block is nonempty
                self.run_statement_block(statement_node.dict['statements'])
        # exit current scope
        self.var_value_stack.pop()

    def run_while_call(self, statement_node):
        ## debugging code
        if statement_node.elem_type != 'while':
            super().error(ErrorType.FAULT_ERROR, "not a while statement")
        ## delete after use

        # create a new scope
        self.var_value_stack.push_scope(InterpreterBase.WHILE_DEF)
        condition = self.evaluate_expression(statement_node.dict['condition'])
        if not isinstance(condition, bool):
            super().error(ErrorType.TYPE_ERROR,
                          """The while condition does not evaluate to boolean value""")
        else:
            while self.evaluate_expression(statement_node.dict['condition']):
                # evaluate the condition every cycle
                self.run_statement_block(statement_node.dict['statements'])
        # exit current scope
        self.var_value_stack.pop()

    def run_return_call(self, statement_node):
        # idea: exit the closest enclosing scope of function
        # if the scope is for if, while statement, that doesn't count
        # idea: recursively pop until we encounter the function scope

        ## debugging code
        if statement_node.elem_type != 'return':
            super().error(ErrorType.FAULT_ERROR, "not a return statement")
        ## delete after use

        ## TO DO ##
        # not only do you pop until encountering the first function block,
        # you must also ensure that the function that contains the return statement node
        # properly returns the value that the return statement node returns.
        #
        # keep popping until we encounter the first InterpreterBase.FCALL_DEF scope
        while self.var_value_stack.curr_scope() != InterpreterBase.FCALL_DEF:
            self.var_value_stack.pop()

        if statement_node.dict['expression'] is None:  # return nil if None
            return None  # return nil if None
        else:
            return copy.deepcopy(self.evaluate_expression(statement_node.dict['expression']))

    def evaluate_expression(self, expression_node):
        # must return the result of evaluation
        # should fork: value, variable, fcall, arithmetic expression
        elemtype = expression_node.elem_type
        if elemtype == InterpreterBase.NIL_DEF: # 'nil'
            return None  # nil in BrewinLang is None in Python
        elif elemtype in ('int', 'string', 'bool'):
            return expression_node.dict['val']
        elif elemtype == 'var': # 'var'
            return self.get_var_value(expression_node)
        elif elemtype == 'neg' or elemtype == '!': # 'neg' or '!'
            return self.evaluate_unary_expression(expression_node)
        # list all possible binary expressions down below
        # equality expression can be used for any data-type operands
        elif elemtype == '==' or elemtype == '!=':
            return self.evaluate_equality_expression(expression_node)
        # separate '+' because it can either be addition or concatenation
        elif elemtype == '+':
            return self.evaluate_plus_sign_expression(expression_node)
        # arithmetic handles arithmetic and comparison operations (binary for integers)
        elif elemtype in ('-', '*', '/', '>', '>=', '<', '<='):
            return self.evaluate_arithmetic_expression(expression_node)
        # logical handles all logical operations (binary for boolean)
        elif elemtype in ('&&', '||'):
            return self.evaluate_logical_expression(expression_node)
        elif elemtype == 'fcall':
            return self.evaluate_func_call_expression(expression_node)
        else:
            super().error(ErrorType.NAME_ERROR, """The node is 
                        not a valid expression""")

    def get_var_value(self, var_node):
        var_name = var_node.dict['name']
        var_value = self.var_value_stack.find_value_of_var(var_name)
        if var_value is not None:
            return var_value
        else:
            super().error(ErrorType.NAME_ERROR,
                          f'The variable {var_name} does not exist')

    def evaluate_unary_expression(self, unary_expression):
        # we should ensure that the unary_expression always gets a node
        # evaluate the expression node under op1
        expression = self.evaluate_expression(unary_expression.dict['op1'])
        if unary_expression.elem_type == 'neg':
            if isinstance(expression, int) and not isinstance(expression, bool):
                # needed because bool is a subclass of int
                return -expression
            else:
                super().error(ErrorType.TYPE_ERROR, """
                    Cannot apply negation (-) to non-integer type expression""")
        elif unary_expression.elem_type == '!':
            if isinstance(expression, bool):
                return not expression
            else:
                super().error(ErrorType.TYPE_ERROR, """
                    Cannot apply negation (!) to non-boolean type expression""")
        else:
            super().error(ErrorType.TYPE_ERROR, """
                Unary operator used on invalid type operand""")

    def evaluate_equality_expression(self, equality_expression_node):
        """debugging code"""
        if equality_expression_node.elem_type not in ('!=', '=='):
            super().error(ErrorType.FAULT_ERROR, "This is not equality-type node!")
        """delete after use"""
        lhs_expression = self.evaluate_expression(equality_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(equality_expression_node.dict['op2'])
        if equality_expression_node.elem_type == '==':
            if type(lhs_expression) != type(rhs_expression):
                return False
            else:
                return lhs_expression == rhs_expression
        else:  # equality_expression_node.elem_type == '!='
            if type(lhs_expression) != type(rhs_expression):
                return True
            else:
                return lhs_expression != rhs_expression

    def evaluate_plus_sign_expression(self, plus_sign_expression_node):
        ## debugging code
        if plus_sign_expression_node.elem_type != '+':
            super().error(ErrorType.FAULT_ERROR, "This is not a plus sign node!")
        ## delete after use
        lhs_expression = self.evaluate_expression(plus_sign_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(plus_sign_expression_node.dict['op2'])
        if isinstance(lhs_expression, int) and isinstance(rhs_expression, int):
            if not isinstance(lhs_expression, bool) and not isinstance(rhs_expression, bool):
                # need this check because bool is a subclass of int
                return self.evaluate_arithmetic_expression(plus_sign_expression_node)
                # return value if the result is an integer
        elif isinstance(lhs_expression, str) and isinstance(rhs_expression, str):
            # return concatenated string
            return self.evaluate_concatenation_expression(plus_sign_expression_node)

    def evaluate_concatenation_expression(self, concatenation_expression_node):
        """debugging code"""
        if concatenation_expression_node.elem_type != '+':
            super().error(ErrorType.FAULT_ERROR, 'Incorrect attempt to evaluate string concatenation node!')
        """delete after use"""
        lhs_expression = self.evaluate_expression(concatenation_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(concatenation_expression_node.dict['op2'])
        # since we already know both are string
        # called by evaluate_plus_sign_expression
        return lhs_expression + rhs_expression

    def evaluate_arithmetic_expression(self, arithmetic_expression_node):
        # This is where TypeError.TYPE_ERROR kicks is
        # since arithmetic operation is supported only for
        # integer values, if any of the operands is string,
        # we should throw an error, otherwise, we should
        # return a correctly evaluated expression result
        """debugging code"""
        if arithmetic_expression_node.elem_type not in ('+', '-', '*', '/', '>', '>=', '<', '<='):
            super().error(ErrorType.FAULT_ERROR, 'Incorrect attempt to evaluate arithmetic expression node!')
        """delete after use"""
        # throw TypeError.TYPE_ERROR if LHS does not evaluate to integer
        lhs_expression = self.evaluate_expression(arithmetic_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(arithmetic_expression_node.dict['op2'])
        if not isinstance(lhs_expression, int) or not isinstance(rhs_expression, int):
            super().error(ErrorType.TYPE_ERROR,
                          'Incompatible types for arithmetic operation')
        elif isinstance(lhs_expression, bool) or isinstance(rhs_expression, bool):
            super().error(ErrorType.TYPE_ERROR,
                          'Cannot compute arithmetic operation to boolean values')
        else:
            if arithmetic_expression_node.elem_type == '+':
                return lhs_expression + rhs_expression
            elif arithmetic_expression_node.elem_type == '-':
                return lhs_expression - rhs_expression
            elif arithmetic_expression_node.elem_type == '*':
                return lhs_expression * rhs_expression
            elif arithmetic_expression_node.elem_type == '/':
                return lhs_expression // rhs_expression
            elif arithmetic_expression_node.elem_type == '>':
                return lhs_expression > rhs_expression
            elif arithmetic_expression_node.elem_type == '>=':
                return lhs_expression >= rhs_expression
            elif arithmetic_expression_node.elem_type == '<':
                return lhs_expression < rhs_expression
            elif arithmetic_expression_node.elem_type == '<=':
                return lhs_expression <= rhs_expression
            else:
                super().error(ErrorType.NAME_ERROR,
                              'Unsupported arithmetic operator')

    def evaluate_logical_expression(self, logical_expression_node):
        if logical_expression_node.elem_type not in ('&&', '||'):
            super().error(ErrorType.FAULT_ERROR, "Incorrect attempt to evaluate logical expression node!")
        # && and || follow strict evaluation rule so both RHS and LHS must be evaluated
        # presumably this is due to facilitate error checking process
        lhs_expression = self.evaluate_expression(logical_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(logical_expression_node.dict['op2'])
        if not isinstance(lhs_expression, bool) or not isinstance(rhs_expression, bool):
            super().error(ErrorType.TYPE_ERROR,
                          'Incompatible types for logical operation')
        else:
            if logical_expression_node.elem_type == '&&':
                return lhs_expression and rhs_expression
            elif logical_expression_node.elem_type == '||':
                return lhs_expression or rhs_expression

    def evaluate_func_call_expression(self, func_call_expression):
        ## for project 2, we should support call to inputi, inputs, and custom-made functions

        """debugging code"""
        if func_call_expression.elem_type != 'fcall':
            super().error(ErrorType.FAULT_ERROR,
                          'Incorrect attempt to evaluate fcall expression node!')
        """delete after use"""

        func_name = func_call_expression.dict['name']
        if func_name == 'inputi':
            # return error if more than one parameter is passed
            # no need to worry here for the case is already handled by the Syntax Error of parse_program()
            if len(func_call_expression.dict['args']) > 1:
                super().error(ErrorType.NAME_ERROR,
                              'No inputi() function found that takes > 1 parameters')
            else:
                if func_call_expression.dict['args']:  # if list is nonempty (nonempty list is True)
                    # print out the passed arguments after evaluation
                    arg = func_call_expression.dict['args'][0]  # take the argument to print out
                    super().output(str(self.evaluate_expression(arg)))
                # receive user input
                # for project 1, we may assume that
                # the user always inputs an integer
                return int(super().get_input())
        elif func_name == 'inputs':
            # call inputs() using get_input() method from intbase.py
            # return str as the return value
            if len(func_call_expression.dict['args']) > 1:
                super().error(ErrorType.NAME_ERROR,
                              'No inputs() function found that takes > 1 parameters')
            else:
                if func_call_expression.dict['args']:  # if list is nonempty (nonempty list is True)
                    # print out the passed arguments after evaluation
                    arg = func_call_expression.dict['args'][0]  # take the argument to print out
                    super().output(str(self.evaluate_expression(arg)))
                # receive user input and return a string
                return super().get_input()
        elif func_name == 'print':
            output_string = ''
            for arg in func_call_expression.dict['args']:
                # args can be any expression nodes
                # including fcall nodes, arithmetic expression nodes, variable nodes, and value nodes
                output_string += str(self.evaluate_expression(arg))
            super().output(output_string)  # use output() for print
            return InterpreterBase.NIL_DEF  # print should return nil
        else:
            # see if the func_name is in the list of custom functions
            # see if the parameter number matches the length of arg of the matching functions
            # to accomplish that, we should use func_arg_dict in the class (name of func and param count)
            # if yes, fetch the function definition and pass the arguments
            # if no, throw ErrorType.NAME_ERROR
            self.run_func_call(func_call_expression)
