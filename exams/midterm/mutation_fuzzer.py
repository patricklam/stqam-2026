from typing import Dict, Tuple, Union, List, Any
import subprocess
import random
from fuzzer import Fuzzer, Runner

class MutationFuzzer(Fuzzer):
    """Base class for mutational fuzzing"""

    def __init__(self, seed: List[str],
                 min_mutations: int = 2,
                 max_mutations: int = 10) -> None:
        """Constructor.
        `seed` - a list of (input) strings to mutate.
        `min_mutations` - the minimum number of mutations to apply.
        `max_mutations` - the maximum number of mutations to apply.
        """
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self) -> None:
        """Set population to initial seed.
        To be overloaded in subclasses."""
        self.population = self.seed
        self.seed_index = 0

    def mutate(self, inp: str) -> str:
        def delete_random_character(s: str) -> str:
            """Returns s with a random character deleted"""
            if s == "":
                return s

            pos = random.randint(0, len(s) - 1)
            # print("Deleting", repr(s[pos]), "at", pos)
            return s[:pos] + s[pos + 1:]

        def insert_random_character(s: str) -> str:
            """Returns s with a random character inserted"""
            pos = random.randint(0, len(s))
            random_character = chr(random.randrange(32, 127))
            # print("Inserting", repr(random_character), "at", pos)
            return s[:pos] + random_character + s[pos:]

        def flip_random_character(s):
            """Returns s with a random bit flipped in a random position"""
            if s == "":
                return s

            pos = random.randint(0, len(s) - 1)
            c = s[pos]
            bit = 1 << random.randint(0, 6)
            new_c = chr(ord(c) ^ bit)
            # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
            return s[:pos] + new_c + s[pos + 1:]    

        """Return inp with a random mutation applied"""
        mutators = [
            delete_random_character,
            insert_random_character,
            flip_random_character
        ]
        mutator = random.choice(mutators)
        return mutator(inp)

    def create_candidate(self) -> str:
        """Create a new candidate by mutating a population member"""
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def fuzz(self) -> str:
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp


def main():
    from random_inputs import is_valid_url
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationFuzzer(seed=[seed_input])

    print(mutation_fuzzer.fuzz())
    print(mutation_fuzzer.fuzz())
    print(mutation_fuzzer.fuzz())

    valid_inputs = set()
    trials = 20
    for i in range(trials):
        inp = mutation_fuzzer.mutate(seed_input)
        if is_valid_url(inp):
            valid_inputs.add(inp)

    print (len(valid_inputs)/trials)

if __name__ == "__main__":
    main()

