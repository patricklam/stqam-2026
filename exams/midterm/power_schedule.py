from Coverage import Location
from typing import List, Sequence
import random

class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str) -> None:
        """Initialize from seed data"""
        self.data = data

        # These will be needed for advanced power schedules
        self.coverage: Set[Location] = set()
        self.distance: Union[int, float] = -1
        self.energy = 0.0

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data

    __repr__ = __str__

class PowerSchedule:
    """Define how fuzzing time should be distributed across the population."""

    def __init__(self) -> None:
        """Constructor"""
        self.path_frequency: Dict = {}

    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assigns each seed the same energy"""
        for seed in population:
            seed.energy = 1

    def normalizedEnergy(self, population: Sequence[Seed]) -> List[float]:
        """Normalize energy"""
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)  # Add up all values in energy
        assert sum_energy != 0
        norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
        return norm_energy

    def choose(self, population: Sequence[Seed]) -> Seed:
        """Choose weighted by normalized energy."""
        self.assignEnergy(population)
        norm_energy = self.normalizedEnergy(population)
        seed: Seed = random.choices(population, weights=norm_energy)[0]
        return seed

def main():
    population = [Seed("A"), Seed("B"), Seed("C")]
    schedule = PowerSchedule()
    hits = { "A": 0, "B": 0, "C": 0 }
    for i in range(10000):
        seed = schedule.choose(population)
        hits[seed.data] += 1
    print (repr(hits))

if __name__ == "__main__":
    main()

