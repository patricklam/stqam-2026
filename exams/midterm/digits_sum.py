from runner import *
from typing import Dict, Tuple, Union, List, Any
import subprocess
import random

Outcome = str

class Fuzzer:
    """Base class for fuzzers."""

    def __init__(self) -> None:
        """Constructor"""
        pass

    def fuzz(self) -> str:
        """Return fuzz input"""
        return ""

    def run(self, runner: Runner = Runner()) \
            -> Tuple[subprocess.CompletedProcess, Outcome]:
        """Run `runner` with fuzz input"""
        return runner.run(self.fuzz())

    def runs(self, runner: Runner = PrintRunner(), trials: int = 10) \
            -> List[Tuple[subprocess.CompletedProcess, Outcome]]:
        """Run `runner` with fuzz input, `trials` times"""
        return [self.run(runner) for i in range(trials)]

class RandomFuzzer(Fuzzer):
    """Produce random inputs."""

    def __init__(self, min_length: int = 10, max_length: int = 100,
                 char_start: int = 32, char_range: int = 32) -> None:
        """Produce strings of `min_length` to `max_length` characters
           in the range [`char_start`, `char_start` + `char_range`)"""
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self) -> str:
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(self.char_start,
                                        self.char_start + self.char_range))
        return out

class MidtermRunner(Runner):
    def run(self, inp: str) -> Tuple[str, Outcome]:
        s = 0
        for c in inp:
            ord_c = ord(c)
            if ord_c >= 48 and ord_c <= 57 and ord_c % 3 == 0:
                s += ord(c) - 48
        if s == 30:
            return (inp, Runner.FAIL)
        else:
            return (inp, Runner.PASS)

def fuzz_midterm_runner():
    mr = MidtermRunner()
    random_fuzzer = RandomFuzzer(char_start=48,char_range=15)
    count = 0
    while True:
        count = count + 1
        inp = random_fuzzer.fuzz()
        result, outcome = mr.run(inp)
        if outcome == mr.FAIL:
            break
    print (result)
    print (count)

if __name__ == "__main__":
    fuzz_midterm_runner()
