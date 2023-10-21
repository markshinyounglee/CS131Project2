from interpreterv1 import *
from brewparse import parse_program


def main():
    testprog_1 = """func main() { 
                    v = 10; 
                    w = v;
                    print("hello"); 
                    print(v);
                    print("hello");
                }"""
    ast1 = Interpreter()
    # ast1.run(testprog_1)
    parsed_test_1 = parse_program(testprog_1)
    # ast1.output(parsed_test_1)
    print(parsed_test_1)


if __name__ == '__main__':
    main()
