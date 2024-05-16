import random
from dataclasses import dataclass
from equipment import Weapon, Armor

@dataclass
class AbilityScores:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


@dataclass
class Character:
    name: str
    race: str
    char_class: str
    level: int
    health: int
    ability_scores: AbilityScores
    weapon: Weapon = None
    armor: Armor = None

