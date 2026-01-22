from fuzzing_campaign import *

if __name__ == "__main__":
    runs = fuzzing_campaign()

    # how many runs don't result in error messages?
    count_no_errors = sum(1 for (data, result) in runs if result.stderr == "")
    print ("# runs: {}".format(len(runs)))
    print ("# no-errors: {}".format(count_no_errors))

    # let's look at the first error message
    errors = [(data, result) for (data, result) in runs if result.stderr != ""]
    (first_data, first_result) = errors[0]

    print ("first error input: {}".format(repr(first_data)))
    print ("stderr output for first error input: {}".format(first_result.stderr))

    # are there any non-error outputs?
    non_errors = [result.stdout for (data, result) in runs if
     "illegal character" not in result.stderr
     and "parse error" not in result.stderr
     and "syntax error" not in result.stderr]
    print ("stdout on non-error runs: {}".format(non_errors))
