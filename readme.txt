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
test_nil.br > wrap all values into value nodes for all data handling (see botom of interpreterv2.py)

Should NOT work:
test_bad_expr2.br
test_bad_cond1.br

Fixed:
test_nested_expr.br
test_concat_str.br
test_recur3.br
test_recur1.br 
test_nested_ret.br


Takeaways:
In my design, the caller of the function creates and destroys the scope before/after entering 
run_func(), which enters the function definition node.

(~4 hours of decoding): catch the exception inside the function body, not the 
statement block body! The error originated from popping the environment scope stack
until the nearest enclosing function scope while run_statement_block() is contained inside
if and while blocks, which would result in popping to occur additionally.

The point of throwing and catching exceptions is for us to implement control flow; that is, 
to exit the enclosing if/while loops and return the value to the caller of the function. 

Thus, the exception handling must occur in run_func() method.
