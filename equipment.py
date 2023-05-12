import random
from dataclasses import dataclass

@dataclass()
class Equipment:
    name: str
    weight: int

@dataclass()
class Weapon(Equipment):
    speed: int
    min_damage: int
    max_damage: int

    def damage_roll(self):
        return random.randint(self.min_damage, self.max_damage)

@dataclass()
class Armor(Equipment):
    speed: int
    protection: int
