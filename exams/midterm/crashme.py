from function_coverage_runner import FunctionCoverageRunner

def crashme(s: str) -> None:
    if len(s) > 0 and s[0] == 'b':
        if len(s) > 1 and s[1] == 'a':
            if len(s) > 2 and s[2] == 'd':
                if len(s) > 3 and s[3] == '!':
                    raise Exception()

def main():
    crashme_runner = FunctionCoverageRunner(crashme)
    crashme_runner.run("good")
    print (list(crashme_runner.coverage()))

if __name__ == "__main__":
    main()

