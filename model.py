
from dataclasses import dataclass
from typing import List, Dict
import json


@dataclass
class Champion:
    """ A champion in the game. It cost golds to buy, and has traits """
    name: str
    traits: List[str]
    cost: int


@dataclass
class Trait:
    """ A trait of a champion. It has a name and a list of tiers, which is the number of champions needed to get the trait. """
    name: str
    tiers: List[int]

    def get_current_tier(self, count: int) -> int:
        """ Get the current tier of the trait for a given number of champions that share the trait"""
        for i, tier in enumerate(self.tiers):
            if tier > count:
                return i
        return len(self.tiers)


def tests():
    trait = Trait('test', [2, 4, 6])
    assert trait.get_current_tier(1) == 0
    assert trait.get_current_tier(2) == 1
    assert trait.get_current_tier(3) == 1
    assert trait.get_current_tier(4) == 2
    assert trait.get_current_tier(5) == 2
    assert trait.get_current_tier(6) == 3
    assert trait.get_current_tier(7) == 3
    assert trait.get_current_tier(8) == 3
    print('Tests passed')


if __name__ == '__main__':
    tests()
