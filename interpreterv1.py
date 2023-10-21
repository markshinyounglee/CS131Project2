# TO BE TURNED IN #
from intbase import *  # import class from module
from brewparse import parse_program


class Interpreter(InterpreterBase):  # TO DO
    def __init__(self, console_output=True, inp=None,
                 trace_output=False):
        super().__init__(console_output, inp)
        # console_output determines where to direct output
        # inp needed for automated testing only
        # trace_output is for debugging purposes
        self.trace_output = trace_output
        # insert more code as needed
        self.variable_name_to_value = {}

    def run(self, program):  # TO DO
        # program is an array of program strings
        # refer to pages 7-8 for pseudocode
        astree = parse_program(program)  # root node
        # returns tree with Element-type nodes
        # TO DO: traverse the tree and evaluate the semantics
        if astree.elem_type != 'function' or astree.dict['functions'] != 'main':
            super().error(ErrorType.NAME_ERROR, """The program
            does not start with the main() function""")
        self.variable_name_to_value = {}  # any method can add member variables
        # map to hold all values to variables
        self.run_func(astree)  # run the function from root

    def run_func(self, func_node):  # execute statements
        for statement in func_node.dict['statements']:
            self.run_statement(statement)  # run all statements

    def run_statement(self, statement_node):  # fork to assignment or fcall
        if statement_node.elem_type == '=':
            self.run_assignment(statement_node)
        elif statement_node.elem_type == 'fcall':
            self.run_func_call(statement_node)
        else:
            super().error(ErrorType.NAME_ERROR, """
            The statement is neither assignment 
            nor function""")

    def run_assignment(self, statement_node):
        target_var_name = statement_node.dict['name']
        expression_name = statement_node.dict['expression']  # maps to expression node
        expression_value = self.evaluate_expression(expression_name)
        # populate the variable map with the current value
        self.variable_name_to_value[target_var_name] = expression_value

    def run_func_call(self, statement_node):
        # for project 1, only print() is considered valid function call statement
        # so fun_func_call always results in console output
        if statement_node.dict['name'] == 'print':
            for arg in statement_node.dict['args']:
                super().output(str(arg))  # use output() for print
        else:
            super().error(ErrorType.NAME_ERROR,
                          f"{statement_node.dict['name']} is not a valid function statement")
        """
        recall that only function used as a statement is
        print, which uses super().output()
        
        In the future, this may have to return value
        but for now, we don't have to return anything
        """

    def evaluate_expression(self, expression_node):
        # must return the result of evaluation
        # should fork: value, variable, fcall, arithmetic expression
        if expression_node.elem_type == 'val':
            return expression_node.dict['val']
        elif expression_node.elem_type == 'var':
            return self.get_var_value(expression_node)
        elif expression_node.elem_type == '+' or expression_node.elem_type == '-':
            return self.evaluate_arithmetic_expression(expression_node)
        elif expression_node.elem_type == 'fcall':
            return self.evaluate_func_call_expression(expression_node)
        else:
            super().error(ErrorType.NAME_ERROR, """The node is 
                        not a valid expression""")

    def get_var_value(self, var_node):
        var_name = var_node.dict['name']
        if var_name in self.variable_name_to_value.keys():
            return self.variable_name_to_value['var_name']
        else:
            super().error(ErrorType.NAME_ERROR,
                          f'The variable {var_name} does not exist')

    def evaluate_arithmetic_expression(self, arithmetic_expression_node):
        # This is where TypeError.TYPE_ERROR kicks is
        # since arithmetic operation is supported only for
        # integer values, if any of the operands is string,
        # we should throw an error, otherwise, we should
        # return a correctly evaluated expression result
        """debugging code"""
        if arithmetic_expression_node.elem_type != '+' or arithmetic_expression_node.elem_type != '-':
            super().error(ErrorType.FAULT_ERROR, 'Incorrect attempt to evaluate arithmetic expression node!')
        """delete after use"""
        # throw TypeError.TYPE_ERROR if LHS does not evaluate to integer
        lhs_expression = self.evaluate_expression(arithmetic_expression_node.dict['op1'])
        rhs_expression = self.evaluate_expression(arithmetic_expression_node.dict['op2'])
        if not isinstance(lhs_expression, int) or not isinstance(rhs_expression, int):
            super().error(ErrorType.TYPE_ERROR,
                          'Incompatible types for arithmetic operation')
        else:
            if arithmetic_expression_node.elem_type == '+':
                return lhs_expression + rhs_expression
            elif arithmetic_expression_node.elem_type == '-':
                return lhs_expression - rhs_expression
            else:
                super().error(ErrorType.NAME_ERROR,
                              'Unsupported arithmetic operator')

    def evaluate_func_call_expression(self, func_call_expression):
        # for project 1, we only need to support call to inputi() function
        """debugging code"""
        if func_call_expression.elem_type != 'fcall':
            super().error(ErrorType.FAULT_ERROR,
                          'Incorrect attempt to evaluate fcall expression node!')
        """delete after use"""

        if func_call_expression.dict['name'] == 'inputi':
            # return error if more than one parameter is passed
            if len(func_call_expression.dict['args']) > 2:
                super().error(ErrorType.NAME_ERROR,
                              'No inputi() function found that takes > 1 parameter')
            else:
                for arg in func_call_expression.dict['args']:
                    # print out the passed arguments after evaluation
                    super().output(str(self.evaluate_expression(arg)))
                    # receive user input
                    # for project 1, we may assume that
                    # the user always inputs an integer
                    return int(super().get_input())
        else:
            super().error(ErrorType.NAME_ERROR,
                          f'No function called {func_call_expression.dict["name"]} found')
