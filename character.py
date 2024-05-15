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
    class_type: str
    level: int
    health: int
    ability_scores: AbilityScores
    weapon: Weapon = None
    armor: Armor = None

    def equip_weapon(self, weapon: Weapon):
        if self.weapon is not None:
            self.unequip_weapon()
        self.weapon = weapon
        print(f'{self.name} equips {self.weapon.name}')

    def unequip_weapon(self):
        self.weapon = None

    def equip_armor(self, armor: Armor):
        if self.armor is not None:
            self.unequip_armor()
        self.armor = armor

    def unequip_armor(self):
        self.armor = None

    def attack(self):
        class_attack_power = {
            'Warrior': self.ability_scores.strength,
            'Rogue': self.ability_scores.dexterity,
            'Wizard': self.ability_scores.wisdom
        }

        # Get the base attack power from the dictionary based on the character's class type
        attack_power = class_attack_power.get(self.class_type, 0)

        # Generate a random multiplier between 0.5 and 1.5
        multiplier = random.uniform(0.5, 1.5)

        # Calculate the final attack power using the random multiplier
        final_attack_power = int(attack_power * multiplier)

        return f"{self.name} attacks with a power of {final_attack_power}!"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return f"{self.name} has been defeated!"
        else:
            return f"{self.name} takes {damage} damage and has {self.health} health remaining."
