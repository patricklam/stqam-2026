from typing import List, Set, Any, Tuple, Dict, Union, Sequence
import random

class Mutator:
    """Mutate strings"""

    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character
        ]
    def insert_random_character(self, s: str) -> str:
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]

    def delete_random_character(self, s: str) -> str:
        """Returns s with a random character deleted"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        return s[:pos] + s[pos + 1:]

    def flip_random_character(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]

    def mutate(self, inp: Any) -> Any:  # can be str or Seed (see below)
        """Return s with a random mutation applied. Can be overloaded in subclasses."""
        mutator = random.choice(self.mutators)
        return mutator(inp)

def main():
    for i in range(10):
        print (repr(Mutator().mutate("A quick brown fox")))
    print (Mutator().mutate("good"))

if __name__ == "__main__":
    main()
