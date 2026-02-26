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

class GreyboxFuzzer(AdvancedMutationFuzzer):
    """Coverage-guided mutational fuzzing."""

    def reset(self):
        """Reset the initial population, seed index, coverage information"""
        super().reset()
        self.coverages_seen = set()
        self.population = []  # population is filled during greybox fuzzing

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if new_coverage not in self.coverages_seen:
            # We have new coverage
            seed = Seed(self.inp)
            seed.coverage = runner.coverage()
            self.coverages_seen.add(new_coverage)
            self.population.append(seed)

        return (result, outcome)

def main():
    import time

    n = 30000
    seed_input = "good"
    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())

    start = time.time()
    greybox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()
    print ("It took the greybox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n))

    _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, crashme)
    gb_max_coverage = max(greybox_coverage)
    print ("Our greybox mutation-based fuzzer covers %d statements." % (gb_max_coverage))

    print (greybox_fuzzer.population)

if __name__ == "__main__":
    main()
