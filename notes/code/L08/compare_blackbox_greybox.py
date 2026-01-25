from typing import Dict, Tuple, Union, List, Any
import subprocess
import random
from fuzzer import Fuzzer, Runner
from mutator import Mutator
from power_schedule import Seed, PowerSchedule
from function_coverage_runner import FunctionCoverageRunner
from population_coverage import population_coverage
from crashme import crashme
from advanced_mutation_fuzzer import AdvancedMutationFuzzer
from greybox_fuzzer import GreyboxFuzzer

def main():
    import time

    n = 30000
    seed_input = "good"

    blackbox_fuzzer = AdvancedMutationFuzzer([seed_input], Mutator(), PowerSchedule())

    start = time.time()
    blackbox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    print ("It took the blackbox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))

    _, blackbox_coverage = population_coverage(blackbox_fuzzer.inputs, crashme)
    bb_max_coverage = max(blackbox_coverage)

    print ("The blackbox mutation-based fuzzer achieved a maximum coverage of %d statements." % bb_max_coverage)

    print ([seed_input] + \
    [\
        blackbox_fuzzer.inputs[idx] for idx in range(len(blackbox_coverage))\
        if blackbox_coverage[idx] > blackbox_coverage[idx - 1]\
    ])

    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())

    start = time.time()
    greybox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()
    print ("It took the greybox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))

    _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, crashme)
    gb_max_coverage = max(greybox_coverage)

    print ("Our greybox mutation-based fuzzer covers %d more statements." % (gb_max_coverage - bb_max_coverage))
    print (greybox_fuzzer.population)

if __name__ == "__main__":
    main()
