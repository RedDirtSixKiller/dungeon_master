#define the valid actions a Cahraacter can take

import random
class Actions:
    def __init__(self):
        pass
    @staticmethod
    def attack(attacker, defender):
        damage = Actions.calculate_damage(attacker, attacker.weapon)
        defender.health -= damage
        print(f"{attacker.name} attacks {defender.name} for {damage} damage!")

    @staticmethod
    def use_item(user, item, target):
        item.use(user, target)

    @staticmethod
    def calculate_damage(attacker, weapon):
        # Calculate damage as a random value within the weapon's damage range
        damage = random.randint(weapon.min_damage, weapon.max_damage)

        # Add the attacker's strength modifier to the damage
        strength_modifier = (attacker.ability_scores.strength - 10) // 2
        damage += strength_modifier

        # Ensure the damage is at least 1
        damage = max(1, damage)

        return damage

