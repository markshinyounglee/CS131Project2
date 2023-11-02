"""
Valid programs
"""
# works!
testing_assignment_1 = """func main() {
                            w = 10;
                            v = 23;   
                        }"""

# works!
testing_print_const_1 = """func main() {
                        print("hello");
                    }
                    """

# works!
testing_print_var_1 = """func main() {
                            v = 10;
                            print(v);
                        }
                        """
# works!
testing_expression_input = """func main() {
                                print(inputi(2+3));
                            }"""

# works!
testing_print_inputted_value_1 = """func main() {
                                        w = inputi("Input a value:");
                                        print("you inputted ", w);
                                    } """

testing_print_inputted_value_2 = """func main() {
                                        print(inputi(""), ": this is what I have");
                                    }"""

testing_inputi_at_end_of_print = """func main() {
                                        print("this is what I have", inputi());
                                    }"""
"""
Invalid programs
"""
wrong_bad_assignment_1 = """func main() {
                        v = 10;
                        print(w);
                    }"""

wrong_no_main_func_1 = """v = 10;
                    print(v);
                    """
wrong_no_main_func_2 = """func {
                            print("hello");
                        }"""
wrong_no_main_func_3 = """func something() {
                            print("hello");
                        }"""

wrong_type_mismatch_1 = """func main() {
                        x = 10;
                        y = "hello";
                        z = x+y;
                    }"""