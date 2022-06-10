from typing import Dict, List
import json

from model import Champion, Trait


def _parse_champion(champion_data: Dict) -> 'Champion':
    """ Parse a champion from a dict coming from the json file """
    name = champion_data['name']
    cost = int(champion_data['cost'])

    # We merge origins and class (called type) names into one list because it has the same format
    traits = champion_data['type']
    traits.extend(champion_data['origin'])

    return Champion(
        name=name,
        traits=traits,
        cost=cost
    )


def _parse_trait(trait_data: Dict) -> 'Trait':
    """ Parse a trait from a dict coming from the json file """
    name = trait_data['name']

    # The tiers are contained in the 'bonus' key
    tiers = []
    for bonus in trait_data['bonus']:
        tiers.append(int(bonus["count"]))

    return Trait(
        name=name,
        tiers=tiers
    )


def parse_traits(path_to_traits: str, path_to_classes: str) -> Dict[str, Trait]:
    """ Read both traits and classes from files and return dict[trait.name] = trait """
    result = {}

    # Read traits
    with open(path_to_traits) as f:
        traits_raw = json.load(f)

    # Parse traits
    for trait_raw in traits_raw:
        trait = _parse_trait(trait_raw)
        result[trait.name] = trait

    # Read classes
    with open(path_to_classes) as f:
        traits_raw = json.load(f)

    # Parse classes
    for trait_raw in traits_raw:
        trait = _parse_trait(trait_raw)
        result[trait.name] = trait

    return result


def parse_champions(path_to_champions: str) -> Dict[str, Champion]:
    """ Read champions from file and return dict[champion.name] = champion """
    result = {}

    # Read champions
    with open(path_to_champions) as f:
        champions_raw = json.load(f)

    # Parse champions
    for champion_raw in champions_raw:
        champion = _parse_champion(champion_raw)
        result[champion.name] = champion

    return result


def filter_by_cost(champions: Dict[str, Champion], cost: int) -> Dict[str, Champion]:
    """ Return a dict of champions with champion.cost <= cost """
    return {
        champion.name: champion
        for champion in champions.values()
        if champion.cost <= cost
    }
