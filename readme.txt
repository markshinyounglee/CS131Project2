Took me around 10 hours
(2 hours reading and annotating the spec thoroughly,
 2.5 hours implementing all the run functions according
 to the provided pseudocode and spec, 3 hours creating
 and running the test cases, 2 hours troubleshooting the
 bug)

No known bugs detected in my program thus far.

There was one bug that kept me bothered for almost two hours, however.
inputi() should not use super().output() when no input is provided,
but I assumed that it does, similar to print(), which led to unexpected
outputs. Barista was very helpful in determining the correct output and
catch recurring erroneous patterns until I figured that the issue was in
printing out the inputi() prompt message. The mysterious empty string
that kept printing out whenever I called inputi() has been troubleshooted.
Now print() should indeed produce an empty string if no input is given,
so that is a major difference between print() and inputi().

# TO BE TURNED IN #
Turn in readme.txt and interpreterv1.py
as well as other supporting Python files.
Do NOT turn in intbase.py nor modify it.
Do NOT submit a .zip file (same for .tar, etc.)

