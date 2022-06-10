from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
from itertools import combinations
import json

from model import Champion, Trait
from utils import parse_traits, parse_champions, filter_by_cost


@dataclass
class Combination:
    champions: List[Champion]
    activated_traits: List[str]
    ranking: int


def main():
    # Some constants
    PATH_TO_CHAMPIONS = 'data/champions.json'
    PATH_TO_ORIGINS = 'data/origins.json'
    PATH_TO_CLASSES = 'data/classes.json'
    COST = 2
    NB_UNITS = 4

    # Read data
    champions = parse_champions(PATH_TO_CHAMPIONS)
    traits = parse_traits(PATH_TO_ORIGINS, PATH_TO_CLASSES)

    # Filter champions by cost
    champions = filter_by_cost(champions, COST)
    print(f'{len(champions)} units with cost <= {COST}')

    # Get all possible combinations of champions
    champions_combinations: List[Champion] = list(
        combinations(champions.values(), NB_UNITS))
    print(f'{len(champions_combinations)} combinations of {NB_UNITS} units')

    # Put that into our dataclass
    all_combinations = [Combination(champions, [], 0)
                        for champions in champions_combinations]

    for i, combination in enumerate(all_combinations):
        # Count each occurence of each trait among the champions
        trait_counts: Dict[str, int] = {}
        for champion in combination.champions:
            for trait in champion.traits:
                if trait not in trait_counts:
                    trait_counts[trait] = 0
                trait_counts[trait] += 1

        # Now find which traits are activated (count > tier threshold)
        combination.activated_traits = [
            trait for trait, count in trait_counts.items()
            if traits[trait].get_current_tier(count) > 0]

        for trait, count in trait_counts.items():
            tier_idx = traits[trait].get_current_tier(count)
            if tier_idx > 0:
                combination.ranking += traits[trait].tiers[tier_idx - 1]

    # Sort by ranking
    all_combinations.sort(key=lambda c: c.ranking, reverse=True)

    # Get the top 10
    top_10 = all_combinations[:100]

    # Print ranking, names and traits
    for combination in top_10:
        names = ' '.join([champion.name for champion in combination.champions])
        traits = ' '.join([trait for trait in combination.activated_traits])
        print(f'{combination.ranking}. {names} - ({traits})')


if __name__ == "__main__":
    main()
