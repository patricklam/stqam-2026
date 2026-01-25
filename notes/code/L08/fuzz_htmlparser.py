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
from counting_greybox_fuzzer import CountingGreyboxFuzzer, AFLFastSchedule
from html.parser import HTMLParser

def my_parser(inp:str) -> None:
    parser = HTMLParser()
    parser.feed(inp)

def main():
    import time

    n = 5000
    seed_input = " "

    blackbox_fuzzer = AdvancedMutationFuzzer([seed_input], Mutator(), PowerSchedule())
    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())
    counting_greybox_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), AFLFastSchedule(5))

    start = time.time()
    blackbox_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    greybox_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    counting_greybox_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    end = time.time()

    print ("It took all three fuzzers %0.2f seconds to generate and execute %d inputs." % (end - start, n))

    _, blackbox_coverage = population_coverage(blackbox_fuzzer.inputs, my_parser)
    bb_max_coverage = max(blackbox_coverage)
    _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, my_parser)
    gb_max_coverage = max(greybox_coverage)
    _, counting_greybox_coverage = population_coverage(counting_greybox_fuzzer.inputs, my_parser)
    cgb_max_coverage = max(counting_greybox_coverage)

    print ("Maximum coverages: %d, %d, %d." % (bb_max_coverage, gb_max_coverage, cgb_max_coverage))
    print ("Last 10 blackbox:")
    print (blackbox_fuzzer.inputs[-10:])
    print ("Last 10 greybox:")
    print (greybox_fuzzer.inputs[-10:])
    print ("Last 10 counting greybox:")
    print (counting_greybox_fuzzer.inputs[-10:])

if __name__ == "__main__":
    main()
