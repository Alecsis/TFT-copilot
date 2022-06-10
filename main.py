from typing import Dict
import pandas as pd
from itertools import combinations
import json

from model import Champion, Type


def parse_types() -> Dict[str, Type]:
    res = {}
    with open('data/types.json') as f:
        types_raw = json.load(f)
    for type_raw in types_raw:
        type = Type.from_dict(type_raw)
        res[type.name] = type
    with open('data/classes.json') as f:
        types_raw = json.load(f)
    for type_raw in types_raw:
        type = Type.from_dict(type_raw)
        res[type.name] = type

    return res


def parse_champions() -> Dict[str, Champion]:
    res = {}
    with open('data/champions.json') as f:
        champions_raw = json.load(f)
    for champion_raw in champions_raw:
        champion = Champion.from_dict(champion_raw)
        res[champion.name] = champion
    return res


def filter_by_cost(champions: Dict[str, Champion], cost: int) -> Dict[str, Champion]:
    return {
        champion.name: champion
        for champion in champions.values()
        if champion.cost <= cost
    }


def main():
    champions = parse_champions()
    types = parse_types()

    cost = 10
    nb_units = 4

    champions = filter_by_cost(champions, cost)
    print(f'{len(champions)} units with cost <= {cost}')

    champions_combinations = list(combinations(champions.values(), nb_units))
    print(f'{len(champions_combinations)} combinations of {nb_units} units')

    all_combinations = {}
    for combination in champions_combinations:
        # For each champion in the combination, increase the type by 1
        types_count = {}
        for champion in combination:
            for type_name in champion.types:
                if not type_name in types_count:
                    types_count[type_name] = 0
                types_count[type_name] += 1

        # For each type, find what level it is
        total_levels = 0
        for type_name, count in types_count.items():
            type = types[type_name]
            level = type.get_current_level(count)
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
