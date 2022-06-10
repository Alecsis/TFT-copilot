
from dataclasses import dataclass
from typing import List, Dict
import json


@dataclass
class Champion:
    name: str
    # id: int
    types: List[str]
    cost: int

    def from_dict(champion_data: Dict) -> 'Champion':
        name = champion_data['name']
        # id = int(champion_data['id'])
        types = champion_data['type']
        types.extend(champion_data['origin'])
        cost = int(champion_data['cost'])

        return Champion(
            name=name,
            # id=id,
            types=types,
            cost=cost
        )


@dataclass
class Type:
    name: str
    levels: List[int]

    def get_current_level(self, count: int) -> int:
        for i, level in enumerate(self.levels):
            if level > count:
                return i
        return len(self.levels)

    def from_dict(type_data: Dict) -> 'Type':
        name = type_data['name']
        levels = []
        for bonus in type_data['bonus']:
            levels.append(int(bonus["count"]))
        return Type(
            name=name,
            levels=levels
        )


def tests():
    type = Type('test', [2, 4, 6])
    print(type.get_current_level(1))
    print(type.get_current_level(3))
    print(type.get_current_level(5))
    print(type.get_current_level(7))


if __name__ == '__main__':
    tests()
