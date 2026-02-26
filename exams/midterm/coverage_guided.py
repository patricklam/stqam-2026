from runner import *
from function_coverage_runner import *
from greybox_fuzzer import *
from mutation_coverage_fuzzer import *
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

def crash_midterm(inp:str) -> None:
    c = 0
    if inp[0] >= '0' and inp[0] <= '9':
        c = min(int(inp[0]), len(inp))
    for i in range(c):
        if inp[i] == 'F':
            raise Exception()
    
def random_fuzz_cg_runner():
    mr = FunctionCoverageRunner(crash_midterm)
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

def mcf_fuzz_cg_runner():
    mr = FunctionCoverageRunner(crash_midterm)
    mcf = MutationCoverageFuzzer(["2FA"])
    mcf.runs(FunctionCoverageRunner(crash_midterm), trials=100000)
    _, mcf_coverage = population_coverage(mcf.population, crash_midterm)
    mcf_max_coverage = max(mcf_coverage)
    print ("Our mutation-based fuzzer covers %d statements." % (mcf_max_coverage))
    print (mcf.population)

def gf_fuzz_cg_runner():
    mr = FunctionCoverageRunner(crash_midterm)
    seed_input = "0"
    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())
    greybox_fuzzer.runs(FunctionCoverageRunner(crash_midterm), trials=30000)
    _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, crash_imdterm)
    gb_max_coverage = max(greybox_coverage)
    print ("Our greybox mutation-based fuzzer covers %d statements." % (gb_max_coverage))
    print (greybox_fuzzer.inputs)
    
if __name__ == "__main__":
    mcf_fuzz_cg_runner()
