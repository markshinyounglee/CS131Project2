Turn in:
- boxtypev2.py: define custom wrapper class
- returnexception.py: define ReturnException for handling return statements
- stackv2.py: define environment stack that stores the stack of dictionaries 
    holding all variables for the current scope
- interpreterv2.py: define the main interpreter logic
- readme.txt: all the explanations 

Failed test cases:

Should work:
test_and_or.br > switch True, False to true, false (use boxtyping?)
## TO DO ##: implement proper box typing using boxtypev2.py (from project 1 solution)

Should NOT work:
test_bad_expr2.br
test_bad_cond1.br

Fixed:
test_nested_expr.br
test_concat_str.br
test_recur3.br
test_recur1.br 
test_nested_ret.br
test_nil.br # wrap all values into value nodes for all data handling (see bottom of interpreterv2.py)


Takeaways:
In my design, the caller of the function creates and destroys the scope before/after entering 
run_func(), which enters the function definition node.

(~4 hours of decoding): I should have caught the exception inside the function body, not the 
statement block body! The error originated from popping the environment scope stack
until the nearest enclosing function scope while run_statement_block() is contained inside
if and while blocks, which would result in popping to occur additionally.

The point of throwing and catching exceptions is for us to implement control flow; that is, 
to exit the enclosing if/while loops and return the value to the caller of the function. 

Thus, the exception handling must occur in run_func() method.

=======================

Also, we should be particularly cautious about return; statement,
because since it doesn't contain a nil literal (like return nil;), 
the parser has None for expression node for return. This has caused some problems
because evaluate_expression_node always assumed that the node passed always
contains elem_type, which caused problems.

To ensure the Brewin boolean values (true and false) and null pointer (nil) prints 
out as it should be, I used the type_valuev1.py included in Carey's solution for project 1.

I changed the name to boxtypev2.py to stress the usage of it as a boxtype.

Internally, all expression evaluations and function operations are done with Python values,
since wrapping and unwrapping each time we do the computation would be too costly.

But the variables in scopes (that is, in environment stack) are all wrapped with Value() class.

The only time we access the variable value is when we get_var_value(), which 
just calls the find_value_of_var() method in stackv2.py. In effect, since environment stack 
is responsible for keeping track of all variables values once all the evalution has been completed,
I primarily only had to concern with wrapping all the variables inside stackv2.py class.


Also, now that we allow nil to be one of the built-in types, we should always 
return whatever value the stack returns. Otherwise, that would be an error. If the program
attempts to access a variable before/after its lifetime, it raises ErrorType.NAME_ERROR
as per the program specifications.