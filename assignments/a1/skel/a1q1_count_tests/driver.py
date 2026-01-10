# This file is not strictly necessary, but I was using it for other reasons.
# You can use it to run the code directly.

from . import count_tests

def main():
    rv = count_tests.tests_in_file_contents(["TEST_CASE", "// nothing", "SCENARIO"])
    print (rv)

if __name__ == "__main__":
    main()
