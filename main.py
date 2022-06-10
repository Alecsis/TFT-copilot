from typing import Dict
import pandas as pd
from itertools import combinations
import json

from model import Champion, Trait
from utils import parse_traits, parse_champions, filter_by_cost


def main():
    champions = parse_champions('data/champions.json')
    traits = parse_traits('data/origins.json', 'data/classes.json')

    cost = 10
    nb_units = 4

    champions = filter_by_cost(champions, cost)
    print(f'{len(champions)} units with cost <= {cost}')

    champions_combinations = list(combinations(champions.values(), nb_units))
    print(f'{len(champions_combinations)} combinations of {nb_units} units')

    all_combinations = {}
    for combination in champions_combinations:
        # For each champion in the combination, increase the trait by 1
        traits_count = {}
        for champion in combination:
            for trait_name in champion.traits:
                if not trait_name in traits_count:
                    traits_count[trait_name] = 0
                traits_count[trait_name] += 1

        # For each trait, find what level it is
        total_levels = 0
        for trait_name, count in traits_count.items():
            trait = traits[trait_name]
            level = trait.get_current_level(count)
            total_levels += level

        names = [champion.name for champion in combination]
        # print(f'{total_levels} levels for combination {names}')

        if total_levels not in all_combinations:
            all_combinations[total_levels] = []

        all_combinations[total_levels].append(names)

    # Get the highest level combination
    max_level = max(all_combinations.keys())
    print(f'Highest level combination: {max_level}')
    for combination in all_combinations[max_level]:
        print(combination)

    # Same for the level below
    sub_level = max_level - 1
    print(f'Sub level combination: {sub_level}')
    for combination in all_combinations[sub_level]:
        print(combination)


if __name__ == "__main__":
    main()
