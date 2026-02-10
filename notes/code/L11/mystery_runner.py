from typing import Tuple, List, Sequence, Any, Optional
from expect_error import ExpectError
from fuzzer import RandomFuzzer, Runner, Outcome

import re

class MysteryRunner(Runner):
    def run(self, inp: str) -> Tuple[str, Outcome]:
        x = inp.find(chr(0o17 + 0o31))
        y = inp.find(chr(0o27 + 0o22))
        if x >= 0 and y >= 0 and x < y:
            return (inp, Runner.FAIL)
        else:
            return (inp, Runner.PASS)

def fuzz_mystery_runner():
    mystery = MysteryRunner()
    random_fuzzer = RandomFuzzer()
    count = 0
    while True:
        count = count + 1
        inp = random_fuzzer.fuzz()
        result, outcome = mystery.run(inp)
        if outcome == mystery.FAIL:
            break
    print (result)
    print (count)

if __name__ == "__main__":
    fuzz_mystery_runner()
