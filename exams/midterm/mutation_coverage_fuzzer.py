from typing import Dict, Tuple, Union, List, Any
import subprocess
import random
from fuzzer import Fuzzer, Runner
from mutation_fuzzer import MutationFuzzer
from function_coverage_runner import FunctionCoverageRunner
from random_inputs import url_consumer

class MutationCoverageFuzzer(MutationFuzzer):
    """Fuzz with mutated inputs based on coverage"""

    def reset(self) -> None:
        super().reset()
        self.coverages_seen: Set[frozenset] = set()
        # Now empty; we fill this with seed in the first fuzz runs
        self.population = []

    def run(self, runner: FunctionCoverageRunner) -> Any:
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if outcome == Runner.PASS and new_coverage not in self.coverages_seen:
            # We have new coverage
            self.population.append(self.inp)
            self.coverages_seen.add(new_coverage)

        return result

if __name__ == "__main__":
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
    urlconsumer_runner = FunctionCoverageRunner(url_consumer)
    mutation_fuzzer.runs(urlconsumer_runner, trials=10000)
    print (mutation_fuzzer.population)
