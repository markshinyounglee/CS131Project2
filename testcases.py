"""
Valid programs
"""
# for project 2

# works!
test_nested_expr = """func main() {
 print((((3+4)*(6/3)))-10);
}"""

# works!
test_overload = """func main() {
  a = 5;
  foo();
  foo(10);
  foo(20,30);
}

func foo() {
  print(a);
}

func foo(a) {
  print(a);
}

func foo(a,b) {
  print(a," ",b);
}"""

test_and_or = """func main() {
  print(true || false && false);
  print(true && true || true && false);
  print(true && true && true && false || false && true && true && true);
}"""

# works!
test_concat_str = """func main() {
  a = "abc" + "def";
  b = "abc";
  c = "def";
  d = b + c;
  print(a);
  print(d);
}"""

# works!
test_dynamic_scoping_2 = """func main() {
  foo(5);
}

func foo(a) {
  print(a);
}"""

test_nested_ret = """func foo() {
  i = 0;
  while (i < 3) {
	j = 0;
    while (j < 3) {
		k = 0;
		while (k < 3) {
			if (i * j * k == 1) {
				return ans;
			} else {
				ans = ans + 1;
				k = k + 1;
			}
		}
		j = j + 1;
	}
	i = i + 1;
  }
}

func main() {
  ans = 0;
  print(foo());
  print(ans);
}"""

test_recur3 = """func main() {
 print(fib(5));
}

func fib(n) {
 if (n < 3) {
  return 1;
 } else {
  return fib(n-2) + fib(n-1);
 }
}"""


##############################################
# for project 1
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