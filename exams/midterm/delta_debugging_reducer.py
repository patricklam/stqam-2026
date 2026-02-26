from typing import Dict, Tuple, Union, List, Any
from runner import *
Outcome = str

class Reducer:
    """Base class for reducers."""

    def __init__(self, runner: Runner, log_test: bool = False) -> None:
        """Attach reducer to the given `runner`"""
        self.runner = runner
        self.log_test = log_test
        self.reset()

    def reset(self) -> None:
        """Reset the test counter to zero. To be extended in subclasses."""
        self.tests = 0

    def test(self, inp: str) -> Outcome:
        """Test with input `inp`. Return outcome.
        To be extended in subclasses."""

        result, outcome = self.runner.run(inp)
        self.tests += 1
        if self.log_test:
            print("Test #%d" % self.tests, repr(inp), repr(len(inp)), outcome)
        return outcome

    def reduce(self, inp: str) -> str:
        """Reduce input `inp`. Return reduced input.
        To be defined in subclasses."""

        self.reset()
        # Default: Don't reduce
        return inp

class CachingReducer(Reducer):
    """A reducer that also caches test outcomes"""

    def reset(self):
        super().reset()
        self.cache = {}

    def test(self, inp):
        if inp in self.cache:
            return self.cache[inp]

        outcome = super().test(inp)
        self.cache[inp] = outcome
        return outcome

class DeltaDebuggingReducer(CachingReducer):
    """Reduce inputs using delta debugging."""

    def reduce(self, inp: str) -> str:
        """Reduce input `inp` using delta debugging. Return reduced input."""

        self.reset()
        assert self.test(inp) != Runner.PASS

        n = 2     # Initial granularity
        while len(inp) >= 2:
            start = 0.0
            subset_length = len(inp) / n
            some_complement_is_failing = False

            while start < len(inp):
                complement = inp[:int(start)] + \
                    inp[int(start + subset_length):]

                if self.test(complement) == Runner.FAIL:
                    inp = complement
                    n = max(n - 1, 2)
                    some_complement_is_failing = True
                    break

                start += subset_length

            if not some_complement_is_failing:
                if n == len(inp):
                    break
                n = min(n * 2, len(inp))

        return inp
