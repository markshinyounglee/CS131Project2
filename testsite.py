from interpreterv2 import *
from brewparse import parse_program
import testcases


def main():
    test = testcases.invalid_arithmetic_2 # invalid_dynamic_scoping_2 
    ast1 = Interpreter()  # already includes parse_program
    ast1.run(test)
    # ast1.output(parsed_test_1)


if __name__ == '__main__':
    main()
