from typing import Dict, Tuple, Union, List, Any, Sequence
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

import pickle   # serializes an object by producing a byte array from all the information in the object
import hashlib  # produces a 128-bit hash value from a byte array

def getPathID(coverage: Any) -> str:
    """Returns a unique hash for the covered statements"""
    pickled = pickle.dumps(sorted(coverage))
    return hashlib.md5(pickled).hexdigest()

class AFLFastSchedule(PowerSchedule):
    """Exponential power schedule as implemented in AFLFast"""

    def __init__(self, exponent: float) -> None:
        self.exponent = exponent

    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = 1 / (self.path_frequency[getPathID(seed.coverage)] ** self.exponent)

class CountingGreyboxFuzzer(GreyboxFuzzer):
    """Count how often individual paths are exercised."""

    def reset(self):
        """Reset path frequency"""
        super().reset()
        self.schedule.path_frequency = {}

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:
        """Inform scheduler about path frequency"""
        result, outcome = super().run(runner)

        path_id = getPathID(runner.coverage())
        if path_id not in self.schedule.path_frequency:
            self.schedule.path_frequency[path_id] = 1
        else:
            self.schedule.path_frequency[path_id] += 1

        return(result, outcome)

def main():
    import time
    n = 10000
    seed_input = "good"
    fast_schedule = AFLFastSchedule(5)
    fast_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), fast_schedule)
    start = time.time()
    fast_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    print ("It took the fuzzer w/ exponential schedule %0.2f seconds to generate and execute %d inputs." % (end - start, n))
    _, counting_greybox_coverage = population_coverage(fast_fuzzer.inputs, crashme)
    cgb_max_coverage = max(counting_greybox_coverage)
    print ("Our fuzzer w/exponential schedule covers %d statements." % (cgb_max_coverage))
    print("             path id 'p'           : path frequency 'f(p)'")
    print (fast_schedule.path_frequency)

    seed_input = "good"
    orig_schedule = PowerSchedule()
    orig_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), orig_schedule)
    start = time.time()
    orig_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    print ("It took the fuzzer w/ original schedule %0.2f seconds to generate and execute %d inputs." % (end - start, n))
    print("             path id 'p'           : path frequency 'f(p)'")
    print (orig_schedule.path_frequency)

    print ('fast schedule:')
    fast_energy = fast_schedule.normalizedEnergy(fast_fuzzer.population)
    for (seed, norm_energy) in zip(fast_fuzzer.population, fast_energy):
        print("'%s', %0.5f, %s" % (getPathID(seed.coverage),
                                   norm_energy, repr(seed.data)))

    print ('original schedule:')
    orig_energy = orig_schedule.normalizedEnergy(orig_fuzzer.population)
    for (seed, norm_energy) in zip(orig_fuzzer.population, orig_energy):
        print("'%s', %0.5f, %s" % (getPathID(seed.coverage),
                                   norm_energy, repr(seed.data)))

    
if __name__ == "__main__":
    main()

